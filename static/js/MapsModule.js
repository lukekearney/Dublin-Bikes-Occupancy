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

	function getMapData(callback){
		var request = window.superagent;
		var url = "http://localhost:5000/api/real-time";
		request.get(url, function(err, response){
			// console.log('Response ok:', response.ok);
			// console.log('Response text:', response.text);
			// need to do more error handling here.
			if (!err){
				var data = JSON.parse(response.text);
				for (var i = 0; i < data.length; i++){
					
					var marker = new google.maps.Marker({
						position: {
							"lat": data[i].lat,
							"lng": data[i].long
						},
						map: settings.mapObj,
						title: data[i].name,
						number: data[i].number
					});

					marker.addListener("click", function(){
						// fetches data based on the marker's number
						BikesModule.getStationHistoricalInformation(this.number, 0);
						var title = this.title.replace(/\(\w+\)/g, "");
						title = this.title.replace(/ /g, "-");

						PageModule.gotoPage("station/" + title.toLowerCase());
						
						//window.location.href = "station/" + title.toLowerCase();
						
					});

					settings.markers.push(marker)
				}
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
			// add each marker to the map
			/*
			for each item in json
				add marker to the map
				add info box
				add marker listeners for charted data
			end for
			*/
		}
	}
}())