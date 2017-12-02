var fs = require('fs');
var ejs = require('ejs');

exports.test = ejs.compile(fs.readFileSync('./Frontend/templates/test.ejs', "utf8"));