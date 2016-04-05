describe("Hello world", function() {
  it("says hello", function() {
    expect(helloWorld()).toEqual("Hello world!");
  });
});


describe("Fetch Station info", function() {
	var res;
	beforeEach(function(done) {
	   BikesModule.getStationInfo("north-circular-road", function(err, result) {
	   	res = result;
	   	done();
	   })
	  });
	

    it("should fetch a numerical station id as part of the result", function(done) {
	    expect(res[0]["number"] > 0 && res[0]["number"] < 101).toBeTruthy();
	    done();
	    
	});
});

describe("Fetch Station historical data", function() {
	var res;
	var errors = 0;
	beforeEach(function(done) {
	    BikesModule.getStationHistoricalInformation(49, 0, function(err, result) {

	   	for (var i = 0; i < result.length; i++) {
	   		if (result[i].day != 0 || result[i].number != 49) {
	   			
	   			errors++;
	   		} else {
	   			console.log("this one is valid");
	   		}
	   	}
	   	done();
	   })
	  });
	

    it("should fetch an array of objects giving occupancy data for the given day and station", function(done) {
	    expect(errors === 0).toBeTruthy();
	    done();
	    
	});
});

describe("Fetch Station historical data by number only", function() {
	var res;
	var valid = true;
	beforeEach(function(done) {
	   BikesModule.getStationHistoricalInformation(49, null, function(err, result) {
	   	res = result;
	   	for (var i = 0; i < result.length; i++) {
	   		if (result[i].day > 6 || result[i].day < 0 || result[i].number != 49) {
	   			valid = false;
	   		}
	   	}
	   	done();
	   })
	  });
	

    it("should fetch an array of objects giving occupancy data for the given station", function(done) {
	    expect(valid).toBeTruthy();
	    done();
	    
	});
});