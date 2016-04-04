// set up IIFE, only exposing the parts we want to be globally accessible
// set up maps module
var PageModule = (function(){
	var currentPage;
	var openPages = {

	}

	var routes = {
		"station" : {
			"pattern": /\/?station\/\d+\/?/,
			callback: function(url, route){
				// request information on that station
				var parts = [];
				for (var i = 0, urlParts = url.split("/"); i < urlParts.length; i++){
					// check not an empty string
					if (urlParts[i].length > 0) {
						parts.push(urlParts[i]);
					} 
				}

				openPages[parts.join("/")] = {
					added: Math.floor(Date.now() / 1000 ),
					visible: true
				};
				console.log(openPages);
				// get the number for the station
				BikesModule.getStationInfo(parts[parts.length - 1], function(err, result){
					// get current day, normalised to Python standard
					var day = (new Date().getDay() + 6) % 7;

					// get data by the number
					var station = result[0];
					var data = BikesModule.getStationHistoricalInformation(station.number, day, function(err, data) {
						// uses error-first callback
						if (!err) {
							renderPage(route, {
								daily: data,
								station: station
							});
						}
						// get current URL for push state
						console.log("/" + parts.join("/"));
						console.log(window.location.pathname);
						history.pushState(window.location.pathname, null, parts.join("/"));
						console.log(window.location.pathname);
						
					});
				});
					
			}
		}
	}

	function renderPage(template, data){
		var template = Handlebars.templates[template];
		var html = template(data);

		document.write(html);
	}

	// public exposed properties
	return {
		gotoStation: function(url){
			for (var route in routes){
				var re = new RegExp(route.pattern, "i", "g");
				if (url.match(re)){
					// fetch data for that station
					routes[route].callback(url, route);
				}
			}
		},

		backPage: function() {
			// toDO: Fill out history API stuff
		}
	}
}());