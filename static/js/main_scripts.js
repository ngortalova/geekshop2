$( document ).on( 'click', '.details a', function(event) {
   console.log(68)
   if (event.target.hasAttribute('href')) {
       var link = event.target.href + 'ajax/';

       var link_array = link.split('/');
       if (link_array[4] == 'category') {
           $.ajax({
               url: link,
               success: function (data) {
                   $('.details').html(data);
               },
           });

           event.preventDefault();
       }
   }
});