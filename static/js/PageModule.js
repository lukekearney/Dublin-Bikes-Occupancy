// set up IIFE, only exposing the parts we want to be globally accessible
// set up maps module
var PageModule = (function(){
	var currentPage;
	var openPages = {

	}

	var routes = {
		"station" : {
			"pattern": /\/?station\/\d+\/?/,
			callback: function(url){
				// request information on that station
				var parts = [];
				for (var i = 0, urlParts = url.split("/"); i < urlParts.length; i++){
					// check not an empty string
					if (urlParts[i].length > 0) {
						parts.append(urlParts[i]);
					} 
				}
				// get the number for the station
				BikesModule.getStationInfo(parts[parts.length - 1], function(err, result){
					// get current day, normalised to Python standard
					var day = (new Date().getDay() + 6) % 7;

					// get data by the number
					var data = BikesModule.getStationHistoricalInformation(number, day, function(err, data) {
						// uses error-first callback
						if (!err) {
							renderPage(route, {
								daily: data,
							});
						}
						
					});
				});
					
			}
		}
	}

	function renderPage(template, data){
		var template = Handlebars.templates[template];
		var html = template(data);

		document.innerHTML = html;
	}

	// public exposed properties
	return {
		gotoStation: function(url, number = null){
			for (var route in routes){
				var re = new RegExp(route, "i", "g");
				if (url.match(re)){
					// fetch data for that station
					
				}
			}
		}
	}
}());