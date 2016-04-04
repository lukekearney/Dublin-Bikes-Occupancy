// set up IIFE, only exposing the parts we want to be globally accessible
// set up maps module
var PageModule = (function(){
	var currentPage;
	var openPages = {

	}
	var state;

	var routes = {
		"station" : {
			"pattern": /\/?station\/\w+\/?/,
			callback: function(url, route){
				// request information on that station
				var parts = [];
				for (var i = 0, urlParts = url.split("/"); i < urlParts.length; i++){
					// check not an empty string
					if (urlParts[i].length > 0) {
						parts.push(urlParts[i]);
					} 
				}

				var glued = parts.join("/");
				if (!openPages[glued]) {
					openPages[glued] = {
						added: Math.floor(Date.now() / 1000 ),
						visible: true,
						id: glued.replace("/", "-")
					};
				} else {
					console.log("page is already open");
				}
				
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
							var node = createNewPageNode(glued);
							var html = renderPage(route, {
								daily: data,
								station: station
							});
							addNewPage(node, html);
						}
						// get current URL for push state
						
						// https://css-tricks.com/using-the-html5-history-api/
						history.pushState(window.location.pathname, null, "/" + parts.join("/"));
						PageModule.setState(history.state);
						console.log(history);
						
						
					});
				});
					
			}
		},
		"home": {
			"pattern": /\/[\w]+/,
			callback: function(url, route){
				// load the home template
				renderPage(route, {
					
				});
				var node = createNewPageNode(url.replace("/", "-"));
				var html = renderPage(route, {
					
				});
				addNewPage(node, html);
				PageModule.setState(history.state);
			}
		}
	}

	function addNewPage(node, html){
		node.innerHTML = html
		document.getElementById("wrapper").appendChild(node);
	}

	function createNewPageNode(data){
		console.log("data is");
		console.log(data);
		var node = document.createElement("div");
		
		// set id of the new node
		node.id = "page-" + data.replace("/", "-");
		return node;
	}

	function renderPage(template, data){
		var template = Handlebars.templates[template];
		var html = template(data);

		return html;
	}

	// public exposed properties
	return {
		gotoPage: function(url){
			console.log("url is " + url);
			for (var route in routes){
				
				var re = new RegExp(routes[route].pattern, "i");
				
				if (re.test(url)){
					console.log("my route is " + route);
					// fetch data for that station
					routes[route].callback(url, route);
					break;
				}
			}


		},

		backPage: function() {
			// toDO: Fill out history API stuff
		},

		getState:function(){
			return state;
		},

		setState: function(s){
			state = s;
		}
	}
}());