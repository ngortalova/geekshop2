from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from geekshop import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200_orig')),
                                                access_token=response['access_token'],
                                                v='5.81')),
                          None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        user.age = age
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_200_orig']:
        # user.avatar_url = data['photo_max_orig']
        photo_path = f'/user_avatars/{user.pk}.jpg'
        photo_full_path = f'{settings.MEDIA_ROOT}{photo_path}'
        photo_data = requests.get(data['photo_200_orig'])
        with open(photo_full_path, 'wb') as photo_file:
            photo_file.write(photo_data.content)
        user.avatar = photo_path


    user.save()
