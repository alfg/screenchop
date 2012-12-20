/*
 * custom.js - Custom built js for various functions.
 * Starring favorites, upvotes/downvotes, tooltips, login/register and annotaions.
 *
 * Author: Alf
 *
 * Copyright (c) 2012 Screenchop
 * 
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *   http://www.github.com/alfg/screenchop
 */


/*
 * Static Document loads. Dynamic loads go in template.
 * */
$(document).ready(function() {
    
    // Init Fancybox
    $('.fancybox').fancybox();

    // Init Target_blank function
    $('.tblank').click(function(){
         window.open($(this).attr('href'));
         return false; 
     });

    // Init tooltips
    $("[rel=tooltip]").tooltip();

    // Init Starring
    $('.star-button').click(starFavorite);

    // Init upvote/downvoting
    $('.upvote-button').click(upvote);
    $('.downvote-button').click(downvote);
    
    // Init Custom Categories Tooltip
    $('#directFullLink').tooltip({placement: 'top'})
    $('#directMedLink').tooltip({placement: 'top'})
    $('#directThumbLink').tooltip({placement: 'top'})
    $('.follow-user-popover').popover({placement: 'bottom'})

    // Init Login/Register submit buttons
    $("#submit").click(submitLoginForm);
    $("#submit2").click(submitRegisterForm);

    // Init Enter button on login/register forms
    $('.loginBoxEnter').keypress(function(e){
        if(e.which == 13){
             submitLoginForm();
         }
    });
    $('.regBoxEnter').keypress(function(e){
        if(e.which == 13){
            submitRegisterForm();
         }
    });

});

/*** All functions below ***/

/* 
 * Starred Favorites 
 * */
function starFavorite() {
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
}

/* 
 * Upvote and downvote buttons on chops pages 
 * */
function upvote() {
    $('.downvote-button').removeClass("highlighted");
    $(this).addClass("highlighted");
    $.ajax({
      type: "POST",
      url: "/upvote",
      data: { chop: $(this).attr('value') }
    }).done(function(msg) {
      //alert( "Data Saved: " + msg );
      if (msg == "upvoted"){
          $('span.votes').html(votes + 1);
      } else if (msg === "upvoted2") {
          $('span.votes').html(votes + 2);
      } else if (msg === "not logged in") {
          $('.upvote-button').removeClass("highlighted");
          alert( "You must be logged in to upvote");
      }
    });
}

function downvote() {
    $('.upvote-button').removeClass("highlighted");
    $(this).addClass("highlighted");
    $.ajax({
      type: "POST",
      url: "/downvote",
      data: { chop: $(this).attr('value') }
    }).done(function(msg) {
      //alert( "Data Saved: " + msg );
      if (msg == "downvoted") {
          $('span.votes').html(votes - 1);
      } else if (msg === "downvoted2") {
          $('span.votes').html(votes - 2);
      } else if (msg === "not logged in") {
          $('.downvote-button').removeClass("highlighted");
          alert( "You must be logged in to downvote");
      }
    });
}

/*
 * Tag Cloud
 * */
function tagcloud() {
    //get tag feed
    $.getJSON("/api/public/tagcloud.json", function(data) {
	    //create list for tag links
	    $("<ul>").attr("id", "tagList").appendTo("#tagCloud");
	    //create tags
	    $.each(data.tags, function(i, val) {
		    //create item
		    var li = $("<li>");
		    //create link
		    $("<a>").text(val.tag).attr({title:"See all pages tagged with " + val.tag, href:"/tags/" + val.tag}).appendTo(li);
		    //set tag size
		    li.children().css("fontSize", (val.freq / 10 < 1) ? val.freq / 10 + 1 + "em": (val.freq / 10 > 2) ? "2em" : val.freq / 10 + "em");
		    //add to list
		    li.appendTo("#tagList");
	    });
    });
}

/*
 * Login and Register functions
 * */

// Checks if Username and/or Password are valid. If valid, redirect back to front page.
function submitLoginForm() {
    var user = $("#username").val();
    var pass = $("#password").val();

    $.ajax({
       type: "POST",
       url: "/login",
       data: { username : user, password : pass }
        }).done(function( msg ) {
            if (msg == 'Success')
            {
                location.reload();
            }
            else {
                $('#login-message').html(msg);
            }
    });
}

function submitRegisterForm() {
    var user = $("#userregister").val();
    var pass = $("#passregister").val();
    var passVerify = $("#passverify").val();
    var tos = $("#tos").attr('checked');
    var invitecode = $("#invitecode").val();

    $.ajax({
       type: "POST",
       url: "/register",
       data: { username : user, password : pass, confirm : passVerify, accept_tos : tos, invite_code : invitecode }
        }).done(function( msg ) {
            if (msg == 'Success')
            {
                location.reload();
            }
            else {
                $('#register-message').empty()
                $.each(msg.errors, function(key, value) { 
                  $('#register-message').append("<li>" + value + "</li>"); 
                });
            }
    });
}


