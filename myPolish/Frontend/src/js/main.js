$(function() {

var Templates = require('./Templates');

$('.main-container').append(Templates.test({username:'user'}));

    $('.fliper-btn').click(function () {
        var card = $('#card');

        if(card.hasClass('flipped')){
            $('.front').css("display", "block");
            $('.back').css("display", "none");
        } else {
            $('.front').css("display", "none");
            $('.back').css("display", "block");
        }
        card.toggleClass('flipped');
    });


    $("#signUp").click(function () {
        var login = $('#signup-username').val();

        var pwd = $('#signup-password').val();
        var data = {
            'username' : login,
            'password' : pwd
        };
        backendPost('/signup/' ,data, function (err, data) {
            if(!err){
                if(data.status==="ok")
                    window.location.href = "/home";
            }
            else
                alert('Error');
        })
    });

    $("#signIn").click(function () {
        var login = $('#signin-username').val();

        var pwd = $('#signin-password').val();
        var data = {
            'username' : login,
            'password' : pwd
        };
        backendPost('/login/', data, function (err, data) {
            if(!err){
                if(data.status==="ok")
                    window.location.href = "/home";
            }
            else
                alert('Error');
        })
    });

    $('#signup-username').on('input', function () {
       validateUsername($('#signup-username').val());
    });

    $('#exit').on('click',function () {
       backendPost('/logout/', null,function () {
           window.location.href='/welcome';
       })
    });
    function validateUsername(username) {
        var data = {
            username : username
        };
        backendPost('/validate_username/',data, function (err, data) {
            if(!err){
                var danger = $('.danger');
                if(!data.valid)
                    danger.show();
                else
                    danger.hide();
            }
            else
                alert('Error');
        })
    }


    function backendPost(url, data, callback) {
        $.ajax({
            headers: {
                'X-CSRFToken' : $('.csrf').text()
            },
            url: url,
            type: 'POST',
            contentType : 'application/json',
            dataType : 'json',
            data: JSON.stringify(data),
            success: function(data){
                callback(null, data);
            },
            error: function() {
                callback(new Error("Ajax Failed"));
            }
        })
    }
});