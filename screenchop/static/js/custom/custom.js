/* Custom Functions go here */

$(document).ready(function() {
    $('.tblank').click(function(){
         window.open($(this).attr('href'));
         return false; 
     });
    $("[rel=tooltip]").tooltip();
});

/* Starred Favorites */
$('.star-button').click(function() {
    $.ajax({
      type: "POST",
      url: "/star",
      data: { chop: $(this).attr('value') }
    }).done(function(msg) {
      //alert( "Data Saved: " + msg );
      if (msg == "starred"){
        $('.star-favorite').addClass("star-starred");
      } else if (msg === "unstarred") {
        $('.star-favorite').removeClass("star-starred");
      } else if (msg === "not logged in") {
        $('.star-favorite').removeClass("star-starred");
        alert( "You must be logged in to star a favorite");
      }
    });
});

