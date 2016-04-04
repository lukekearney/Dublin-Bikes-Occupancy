// set up IIFE, only exposing the parts we want to be globally accessible
// set up maps module
var PageModule = (function(){
	var currentPage;
	var openPages = {

	}

	function renderPage(template, data){
		var template = Handlebars.templates[template];
		var html = template(data);
		document.innerHTML = html;
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
		}

		gotoPage: function(url){
			
		}
	}
}())