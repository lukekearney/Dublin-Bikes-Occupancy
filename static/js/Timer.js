// https://developer.mozilla.org/en-US/docs/Web/API/WindowTimers/clearTimeout
var Timer = function(action, interval) {
    this.action = action;
    // converts interval from seconds to milliseconds
    this.interval = interval * 1000;
};

Timer.prototype = {
  setup: function() {
      var self = this;
      if (typeof this.timeoutID === "number") {
          this.cancel();
      } else {
          this.timeoutID = window.setTimeout(function(msg) {
              self.action();
          }, this.interval);
      }
  },

  cancel: function() {
      window.clearTimeout(this.timeoutID);
      this.timeoutID = undefined;
  }
}
