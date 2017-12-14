var Templates = require('./Templates');
var Lessons = require("./lessons");
var Tests = require("./test");

var $temp = $('#template');
var $nodeMap;
var API = require('./API');


function initialise(data) {
    $temp.html('');
    var lessons = Templates.Lessons_Map({title:'Уроки', lessons: data.lessons, tests: data.tests, level: data.level});
    $nodeMap = $(lessons);

    $temp.append($nodeMap);
    f(data.level);
}
function f(level) {

    $nodeMap.find('.l.click-td').click(function () {
        var num = $(this).attr("id");
        if (num > level) {
            var id = '#' + num + 'img';
            $(id).effect("pulsate", {times: 1}, 1500);
            return;
        }

        var data = {
            'num': num
        };
        API.backendPost('/api/lesson/', data, function (err, data) {
            if (!err) {
                if (data.status === "ok") {
                    if (data.type === "grammar")
                        Lessons.grammarTemp(data);
                    else {
                        Lessons.dictionaryTemp(data);
                    }
                }
            }
            else
                alert('Error');
        });
    });

    $nodeMap.find('.t.click-td').click(function () {
        var num = $(this).attr("id");
        var data = {
            'num': num
        };
        API.backendPost('/api/test/', data, function (err, data) {
            if (!err) {
                if (data.status === "ok")
                    Tests.testTemp(data);
            }
            else
                alert('Error');
        });

    });
}

exports.initialiseMap = initialise;