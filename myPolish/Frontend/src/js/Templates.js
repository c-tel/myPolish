var fs = require('fs');
var ejs = require('ejs');

exports.Lessons_Map = ejs.compile(fs.readFileSync('./Frontend/templates/Lessons_Map.ejs', "utf8"));
exports.Grammar_Lesson = ejs.compile(fs.readFileSync('./Frontend/templates/Grammar_Lesson.ejs', "utf8"));