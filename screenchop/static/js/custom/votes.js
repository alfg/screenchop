$('.upvote-button').click(function(){
    $('.downvote-button').removeClass("highlighted");
    $(this).addClass("highlighted");
    $.ajax({
      type: "POST",
      url: "/upvote",
      data: { chop: $(this).attr('value') }
    }).done(function( msg ) {
      //alert( "Data Saved: " + msg );
      if (msg == "upvoted"){
      $('span.votes').html(votes + 1);
      } else if (msg == "upvoted2"){
      $('span.votes').html(votes + 2);
      }
    });
});

$('.downvote-button').click(function(){
    $('.upvote-button').removeClass("highlighted");
    $(this).addClass("highlighted");
    $.ajax({
      type: "POST",
      url: "/downvote",
      data: { chop: $(this).attr('value') }
    }).done(function( msg ) {
      //alert( "Data Saved: " + msg );
      if (msg == "downvoted"){
      $('span.votes').html(votes - 1);
      } else if (msg == "downvoted2"){
      $('span.votes').html(votes - 2);
      }
    });
});
