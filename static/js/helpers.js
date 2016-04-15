function getColour(decimal) {
	var dec = parseInt("ffffff", 16);
	var colour = Math.round(255 * decimal)
	
	var hex = colour.toString(16);
	
	return "rgb(255, " + colour + ", 0)";
	//console.log(hex);
	//return "#ff" + hex + "00";
}

// http://stackoverflow.com/questions/3710204/how-to-check-if-a-string-is-a-valid-json-string-in-javascript-without-using-try/3710226
function isJSON(str) {
	try {
		JSON.parse(str);
	} catch (e) {
		return false;
	}
	return true;
}