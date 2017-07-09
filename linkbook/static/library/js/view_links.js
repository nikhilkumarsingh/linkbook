$(function () {

          var cards = $('.card_link');

            cards.click(function () {
                var id = this.id;
                var url = '/link/' + id;
                window.location.href = url;
            });

            $('.collapsible').collapsible();
          //  $('.collapsible').collapsible('destroy');

            $('.dropdown-button').dropdown({
                inDuration: 300,
                outDuration: 225,
                  constrainWidth: false, // Does not change width of dropdown to that of the activator
                  hover: false, // Activate on hover
                  gutter: 0, // Spacing from edge
                  belowOrigin: true, // Displays dropdown below the button
                  alignment: 'left', // Displays dropdown with edge aligned to the left of button
                  stopPropagation: true // Stops event propagation

    });

         $('.modal').modal({
          dismissible: true, // Modal can be dismissed by clicking outside of the modal
          opacity: .5, // Opacity of modal background
          inDuration: 300, // Transition in duration
          outDuration: 200, // Transition out duration
          startingTop: '4%', // Starting top style attribute
          endingTop: '10%', // Ending top style attribute
          ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
           // alert("Ready");
            // console.log(modal, trigger);
           // $('.collapsible').collapsible();
            $('.collapsible').collapsible('destroy');
          },
          complete: function() { //alert('Closed');

              $('.collapsible').collapsible();
               } // Callback for Modal close
        }
      );


         $('.collapsible-header #infoUniversal').click(function (e) {

        e.stopPropagation();
        Materialize.toast('This is universal book. It contains all of your links. It cant be edited or modified in any way.', 10000,'',function ()
        {
         //  $('.collapsible').collapsible();
        });

    });

   $('.dropdown_links').click(function (e) {

       e.stopPropagation();
       var id = $(this).attr('href');
       // console.log(id);
       $(id ).modal('open');

   });

   $('.optionsButton').click(function (e) {

       e.stopPropagation();

   })

});