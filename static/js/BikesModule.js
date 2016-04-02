var BikesModule = (function(){
	function filterData(data){

	}

    return {
        getStationHistoricalInformation: function(number){
        	var url = "http://localhost:5000/api/station/" + number;
        	
            request.get(url, function(err, response){
				// console.log('Response ok:', response.ok);
				// console.log('Response text:', response.text);
				// need to do more error handling here.
				if (!err){
					var data = JSON.parse(response.text);
					console.log(data);
					// return the station data
				}
			});
        }

    }
}())