// set up IIFE, only exposing the parts we want to be globally accessible
// set up maps module
var MapsModule = (function(){
	// allow referencing of the entire maps module
	var self = this;

	// private object property, available to the MapsModule
	var settings = {
		"map": null,
		"markers": []
	}

	// private method
	function setUpMap(){
		
		var map;

		// insert the google map object
	    map = new google.maps.Map(settings.map, {
			center: {lat: 53.3474000259898, lng: -6.259202954653347},
			zoom: 13
        });

        settings.mapObj = map;

	}

	// http://stackoverflow.com/questions/7095574/google-maps-api-3-custom-marker-color-for-default-dot-marker/18623391#18623391
	function pinSymbol(color) {
		// console.log(color);
	    return {
	        path: 'M 0,0 C -2,-20 -10,-22 -10,-30 A 10,10 0 1,1 10,-30 C 10,-22 2,-20 0,0 z M -2,-30 a 2,2 0 1,1 4,0 2,2 0 1,1 -4,0',
	        fillColor: color,
	        fillOpacity: 1,
	        strokeColor: '#ffcc00',
	        strokeWeight: 1,
	        scale: 1,
	   };
	}

	function placeMarkers (response) {
		var data = response;
		console.log("REAL TIME:" + data.length);
		for (var i = 0; i < data.length; i++){

			var marker = new google.maps.Marker({
				position: {
					"lat": data[i].lat,
					"lng": data[i].long
				},
				map: settings.mapObj,
				title: data[i].name,
				number: data[i].number,
				icon: pinSymbol(getColour(data[i].available_bikes / data[i].bike_stands)),
			});


			marker.addListener("click", function(){
				// fetches data based on the marker's number
				BikesModule.getStationHistoricalInformation(this.number, 0);
				var title = this.title.replace(/\(\w+\)/g, "");
				title = this.title.replace(/ /g, "-");
				window.location.href = "/station/" + title.toLowerCase();
			});

			settings.markers.push(marker)
		}
	}

	function getMapData(callback){

		BikesModule.getRealTimeData(function(err, response){
			if (!err){
				
				placeMarkers(response);
			}
		});


		//based on http://www.w3schools.com/ajax/tryit.asp?filename=tryajax_get
		// var xmlhttp = new XMLHttpRequest();
		// var url = "https://localhost:5000/api/static";


		// xmlhttp.onreadystatechange = function () {
		// 	if (xmlhttp.readyState === 4 && xmlhttp.status == 200) {
		// 		// success
		// 		// check if callback function is defined
		// 		if (callback){
		// 			// run callback
		// 			callback(xmlhttp.response);
		// 		} else {
		// 			// default response to successful request
		// 			console.log("Request completed successfully: ");
		// 			console.log(response);

		// 		}
		// 	} else if (xmlhttp.readyState === 4 && (xmlhttp.status >= 400 || xmlhttp.status < 500)){
		// 		// error handling
		// 		console.log("uh oh");
		// 		console.error(xmlhttp.statusText);
		// 	}
		// }
		// xmlhttp.open("GET", url, true);

		// xmlhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
		// xmlhttp.setRequestHeader("Accept-Language", "en-US,en;q=0.8");
		// xmlhttp.setRequestHeader("Pragma", "no-cache");

		// xmlhttp.send();

	}

	// public exposed properties
	return {
		init: function(element){
			settings.map = element;
			// set up the map
			setUpMap();

			// call getMapData with the callback function
			getMapData(function(resp){
				console.log(resp);
			});
		},

		addMarkers: function(json){
			placeMarkers(json);
		}
	}
}())