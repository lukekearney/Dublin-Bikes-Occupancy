var BikesModule = (function(){
	// https://addyosmani.com/resources/essentialjsdesignpatterns/book/#modulepatternjavascript

	function hasStoredRealTime(station = null) {
		// load the data using the cache module
		// clear cache first
		CacheModule.removeExpired();
		var loaded = CacheModule.load("real-time");
		if (loaded == null) {
			return false;
		} 

		return true;

	}
	
	function saveRealTime(data) {
		CacheModule.save("real-time", data, 60);
	}

    return {
        getStationHistoricalInformation: function(number, day = null, callback = null){
        	var request = window.superagent;	
        	var url = "/api/station/" + number;
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
			});

        },



        getStationInfo: function(address, callback = null) {
        	var request = window.superagent;
        	address = address.replace(/ /g, "-");
        	// ensure its the correct format
        	var url = "/api/station-info/" + address;

  
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
        },

        getRealTimeData: function(callback) {
        	
        	var request = window.superagent;
        	CacheModule.removeExpired();
        	
        	if (!hasStoredRealTime()) {
        		var url = "/api/real-time";
        		
				request.get(url, function(err, response){
					// console.log('Response ok:', response.ok);
					// console.log('Response text:', response.text);
					// need to do more error handling here.
					if (!err) {
						var json = JSON.parse(response.text)
						callback(err, json);
						saveRealTime(json);
					}

				});
			} else {

        		
	        	var data = CacheModule.load("real-time");
	        	
	        	callback(null, data);

        	}
    	}

    }
}())
