$('.upvote-button').click(function(){
    $('.downvote-button').removeClass("highlighted");
    $(this).addClass("highlighted");
    $.ajax({
      type: "POST",
      url: "/upvote",
      data: { chop: $(this).attr('value') }
    }).done(function( msg ) {
      //alert( "Data Saved: " + msg );
      $('span.votes').html(votes + 1);
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
      $('span.votes').html(votes - 1);
    });
});
