var page = require('webpage').create();

page.onConsoleMessage = function(msg){
	console.log(msg);
};

page.open('https://www.pornhub.com', function(status){
		var title = page.evaluate(function(){
			console.log(document.title);
		});
		page.render('pornhub.png');
		phantom.exit();
	});