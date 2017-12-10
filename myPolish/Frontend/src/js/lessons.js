var Templates = require('./Templates');
var $temp = $('#template');
var $nodeMap;


function initialise() {
    var lessons = Templates.Lessons_Map({title:'Уроки'});
    $nodeMap = $(lessons);

    $temp.append($nodeMap);
    f();
}
//function grammarTemp(data) {
function grammarTemp() {
    $temp.html("");
    var html_code = Templates.Grammar_Lesson({title:'Перші кроки'});
    var $nodeGr = $(html_code);
    $temp.append($nodeGr);
}
function f() {
    $nodeMap.find('#less01').click( function () {
        // var data = {
        //     'number' : 1
        // };
        // backendPost('/api/lesson' ,data, function (err, data) {
        //     if(!err){
        //         if(data.status==="ok")
        //             grammarTemp(data);
        //     }
        //     else
        //         alert('Error');
        // })
        grammarTemp();
    });
    // $temp.append($nodeMap);
}

// $('#less01').click( function () {
//     // var data = {
//     //     'number' : 1
//     // };
//     // backendPost('/api/lesson' ,data, function (err, data) {
//     //     if(!err){
//     //         if(data.status==="ok")
//     //             grammarTemp(data);
//     //     }
//     //     else
//     //         alert('Error');
//     // })
//     alert("click!");
//     grammarTemp();
// });


exports.initialiseLessons = initialise;