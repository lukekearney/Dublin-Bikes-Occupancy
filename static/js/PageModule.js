// set up IIFE, only exposing the parts we want to be globally accessible
// set up maps module
var PageModule = (function(){
	var currentPage;
	var openPages = {

	}
	var state;
	var stationPrefix = "station/"
	function updateContent(data) {
      if (data == null)
        return;

      contentEl.textContent = data.content;
      photoEl.src = data.photo;
    }

    // Load some mock JSON data into the page
    function clickHandler(event) {
      var cat = event.target.getAttribute('href').split('/').pop(),
          data = cats[cat] || null; // In reality this could be an AJAX request

      updateContent(data);

      // Add an item to the history log
      history.pushState(data, event.target.textContent, event.target.href);

      return event.preventDefault();
    }

    // Attach event listeners
    for (var i = 0, l = linkEls.length; i < l; i++) {
      linkEls[i].addEventListener('click', clickHandler, true);
    }

    // Revert to a previously saved state
    window.addEventListener('popstate', function(event) {
      console.log('popstate fired!');

      updateContent(event.state);
    });

    // Store the initial content so we can revisit it later
    history.replaceState({
      content: contentEl.textContent,
      photo: photoEl.src
    }, document.title, document.location.href);

	// public exposed properties
	return {
		gotoPage: function(url, push=true){
			//https://css-tricks.com/using-the-html5-history-api/
			// if it matches a station pattern, get that station
			var re = new RegExp(/\/?station\/\w+\/?/, "i");
			
			if (url != null && url != "/"){
				// check if the required prefix is not presents
				// if (url.indexOf(stationPrefix) == -1) {
				// 	// add it onto the url
				// 	url = stationPrefix + url;
				// }
				console.log("Is this is? " + url);
				
				// get the number for the station
				var ident = url.replace(stationPrefix, "");
				BikesModule.getStationInfo(ident, function(err, result){
					// get current day, normalised to Python standard
					var day = (new Date().getDay() + 6) % 7;

					// get data by the number
					var station = result[0];
					
					var data = BikesModule.getStationHistoricalInformation(station.number, day, function(err, data) {
						// uses error-first callback

						if (!err) {
							console.log("loading station");
							var node = createNewPageNode(ident);
							var html = renderPage("station", {
								daily: data,
								station: station
							});
							addNewPage(node, html);
							if (push) {
								console.log("pushing");
								history.pushState(ident, null, url);
							}
							
						}
						// get current URL for push state
						
						// https://css-tricks.com/using-the-html5-history-api/
						
						
						
					});
				});
				
			} else {
				// if not, get home
				var node = createNewPageNode("default");
				var html = renderPage("home", {
					
				});
				addNewPage(node, html);

				MapsModule.init(document.getElementById("map"));
			}
			
			
			// for (var route in routes){
				
			// 	var re = new RegExp(routes[route].pattern, "i");
			// 	console.log(re.test(url));
			// 	if (re.test(url)){
			// 		console.log("my route is " + route);
			// 		// fetch data for that station
			// 		routes[route].callback(url, route);
			// 		break;
			// 	}
			// }


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