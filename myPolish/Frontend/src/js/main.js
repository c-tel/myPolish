$(function() {
    var Map = require("./map");
    var Welcome = require('./welcome.js');
    var API = require('./API');
    var Templates = require('./Templates');

     if(window.location.href.indexOf('home') !== -1) {
        API.backendPost('/api/init/', {}, function (err, data) {
            if (!err)
                Map.initialiseMap(data);
        });
    }

    $('#exit').on('click',function () {
       API.backendPost('/logout/', null,function () {
           window.location.href='/welcome';
       })
    });
    $('#info_trigger').on('click', function () {
        API.backendPost('/api/day/', {}, function (err, data) {
            var code = Templates.Info({count: data.count});
            $('#modal_window').append(code);
            $('#close').click(function () {
                $('#modal_window').html('');
            });
            $('#shareBtn').on('click', function() {
                alert('click!');
                var obj = {
                    "og:title" : 'Сьогодні я вивчив ' + data.count + ' слів польською з My Polish!',
                    "og:url" : "http://google.com/",
                    "og:type" : "Object"
                };
                FB.ui({
                    method: 'feed',
                    display: 'popup',
                    app_id : 408371692927964,
                    object: JSON.stringify(obj),
                    href: 'https://google.com/'
                }, function(response){});
            });
        });
    });
});