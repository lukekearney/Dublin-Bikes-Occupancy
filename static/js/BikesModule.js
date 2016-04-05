var BikesModule = (function(){
	function filterData(data){

	}

    return {
        getStationHistoricalInformation: function(number, day = null, callback = null){
        	var request = window.superagent;	
        	var url = "http://localhost:5000/api/station/" + number;
        	console.log(day);
        	if (day != null){
        		url += "/" + day;
        	}
        	

            request.get(url, function(err, response){
				// console.log('Response ok:', response.ok);
				// console.log('Response text:', response.text);
				// need to do more error handling here.
				if (!err){
					var data = JSON.parse(response.text);
					
					// return the station data
					if (callback){
						callback(null, data);
					}

					return data;
				} else {
					if (callback) {
						callback (err, response.text);
						return response.text;
					}

				}

				callback(null, []);
			});
			
        },

        getStationInfo: function(address, callback = null) {
        	var request = window.superagent;

        	// ensure its the correct format
        	address = address.replace(" ", "-");
        	var url = "http://localhost:5000/api/station-info/" + address;
        	request.get(url, function(err, response){
        		if (!err) {
        			
        			var data = JSON.parse(response.text);
        			if (callback) {
        				callback(null, data);
        			}
        		} else {
        			console.error(response.text);
        		}
				
			});
        }

    }
}())