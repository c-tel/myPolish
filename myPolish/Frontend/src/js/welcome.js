var API = require('./API');

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
    API.backendPost('/signup/' ,data, function (err, data) {
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
    API.backendPost('/login/', data, function (err, data) {
        if(!err){
            if(data.status==="ok")
                window.location.href = "/home";
            else {
                $('#error').css('visibility', 'visible');
            }
        }
        else
            alert('Error');
    })
});
$('#signup-username').on('input', function () {
    validateUsername($('#signup-username').val());
});
function validateUsername(username) {
    var data = {
        username : username
    };
    API.backendPost('/validate_username/',data, function (err, data) {
        if(!err){
            var danger = $('.danger');
            if(!data.valid)
                danger.css('visibility', 'visible');
            else
                danger.css('visibility', 'hidden');
        }
        else
            alert('Error');
    })
}