var CacheModule = (function() {
    var prefix = "dbbikes-";

    // set up the time to clear expired items in cache. Runs every hour
    var clearExpiredTimer = new Timer(function(){
        this.cancel();
        clearExpired();
        
        this.setup();
    }, 60);
    clearExpiredTimer.setup();

    function exists(key) {
        if (getItem(key)) {
            return true;
        } else {
            return false;
        }
    }

    function clearExpired(key = null){
        // removes old data from cache, if it has expired. The optional key can be supplied to only target specific storage
        if (window.localStorage) {
            var currentTime = Math.floor(Date.now() / 1000);
            var data;
            
            if (key) {
                // check if the key exists
                if (exists(key)) {  
                    // check if it has expired
                    data = JSON.parse(getItem(key));
                    if (data.expires) {
                        // if the current time is higher than the expiry time in the data
                        if (data.expires <= currentTime) {
                            // delete from localStorage
                            removeItem(key);
                            // return true if removed
                            return true;
                        } else {
                            //console.log(key + " has not expired");
                            // return false if not expired
                            return false;
                        }
                    }

                } else {
                    console.error("Cannot check expiry of item ("+ key +") that doesn't exist")
                }
            } else {
                var removeItems = [];
                // http://stackoverflow.com/questions/8419354/get-html5-localstorage-keys
                for (var i = 0; i < localStorage.length; ++i) {
                    // check if the key was set by this application (using the prefix above)
                    var re = new RegExp(prefix + ".+");
                    
                    if (localStorage.key(i).match(re)){
                        var key = localStorage.key(i).substring(prefix.length);
                        console.log("key is: " + key);
                        // recursively call to remove this key. Check if its removed
                        if(clearExpired(key)){
                            // decrement i to account for removed element
                            i--;
                        }
                    }
                    
                }
            }
        } else {
            alert("Local Storage is not supported in this browser");
        }
    }

    // small abstractions
    function getItem(key){
    	return localStorage.getItem(prefix + key);
    }

    function setItem(key, value){
    	return localStorage.setItem(prefix + key, value);
    }

    function removeItem(key){
    	return localStorage.removeItem(prefix + key);
    }

    return {
        save: function(key, value, expires) {
            // saves into local storage
            // check if localStorage is supported
            if (window.localStorage) {
                // check if it exists in cache already and updates data if needs be
                var data;
                // calculates expiry time
                var expiryTime = Math.floor(Date.now() / 1000) + expires;


                data = {
                    expires: expiryTime,
                    value: value
                }

                // add the value
                setItem(key, JSON.stringify(data));
                
            } else {
                alert("Local Storage is not supported in this browser");
            }

        },

        load: function(key) {
            // loads from cache
            if (window.localStorage) {
                // check if it exists already
                clearExpired();
                if (!exists(key)){
                    return null;
                }

                data = getItem(key);
                if (isJSON(data)) {
                    var currentTime = Math.floor(Date.now() / 1000);
                    data = JSON.parse(data);
                }
                
                return data.value;
            } else {
                alert("Local Storage is not supported in this browser");
            }
        },

        removeExpired: function(key = null) {
            clearExpired(key);
        },
    }
}())
