/*
 * login.js - Custom built js for the login process of Screenchop.
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


// Dynamically clears username and password boxes when focus.
$(document).ready(function loginForm() {

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

$("#submit").click(submitLoginForm);

$('.loginBoxEnter').keypress(function(e){
      if(e.which == 13){
       submitLoginForm();
       }

      });

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

$("#submit2").click(submitRegisterForm);

$('.regBoxEnter').keypress(function(e){
      if(e.which == 13){
       submitRegisterForm();
       }

      });

// End (document).ready()
});
