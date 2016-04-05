describe("Hello world", function() {
  it("says hello", function() {
    expect(helloWorld()).toEqual("Hello worldy!");
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
	

    it("should support async execution of test preparation and expectations", function(done) {
	    expect(res).toBeGreaterThan(0);
	    done();
	    
	});
})