var Templates = require('./Templates');
var $temp = $('#template');
var $nodeMap;
var API = require('./API');


function initialise() {
    var lessons = Templates.Lessons_Map({title:'Уроки'});
    $nodeMap = $(lessons);

    $temp.append($nodeMap);
    f();
}
function grammarTemp(data) {
    alert(data.srcs);
    $temp.html("");
    var html_code = Templates.Grammar_Lesson({title:'Перші кроки'});
    var $nodeGr = $(html_code);
    $temp.append($nodeGr);
}
function f() {
    $nodeMap.find('.click-td').click( function () {
        var num = $(this).attr("id");
        var data = {
            'num' : num
        };
        API.backendPost('/api/lesson/' ,data, function (err, data) {
            if(!err){
                if(data.status==="ok")
                    grammarTemp(data);
            }
            else
                alert('Error');
        });
        grammarTemp();
    });
}

exports.initialiseLessons = initialise;