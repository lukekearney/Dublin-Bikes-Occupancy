// set up IIFE, only exposing the parts we want to be globally accessible
   		(function(global){
   			// set up maps module
   			var MapsModule = (function(){
   				// allow referencing of the entire maps module
   				var self = this;

   				// private object property, available to the MapsModule
   				var settings = {
   					"map": document.getElementById("map"),
   				}
				
   				// private method
				function setUpMap(){
					
					var map;

					// insert the google map object
				    map = new google.maps.Map(settings.map, {
						center: {lat: 53.3474000259898, lng: -6.259202954653347},
						zoom: 13
			        });

				}

				function getMapData(callback){
					//based on http://www.w3schools.com/ajax/tryit.asp?filename=tryajax_get
					var xmlhttp = new XMLHttpRequest();
					var url = "https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=5a523b8e0346cd6360130dd031e990283bfb9c8b";
					

					xmlhttp.onreadystatechange = function () {
						if (xmlhttp.readyState === 4 && xmlhttp.status == 200) {
							// success
							// check if callback function is defined
							if (callback){
								// run callback
								callback(xmlhttp.response);
							} else {
								// default response to successful request
								console.log("Request completed successfully: ");
								console.log(response);
								
							}
						} else if (xmlhttp.readyState === 4 && (xmlhttp.status >= 400 || xmlhttp.status < 500)){
							// error handling
							console.error(xmlhttp.statusText);
						}
					}
					xmlhttp.open("GET", url, true)
					xmlhttp.send()
				}

				// public exposed properties
				return {
					init: function(phrase){
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

   			// initialise the application
   			global.initialise = function(){
   				MapsModule.init();
   			}
   		}(window));