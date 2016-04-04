(function() {
  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};
templates['home'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    return "<h1>HOME</h1>";
},"useData":true});
templates['station'] = template({"compiler":[7,">= 4.0.0"],"main":function(container,depth0,helpers,partials,data) {
    var stack1;

  return "<h1>"
    + container.escapeExpression(container.lambda(((stack1 = (depth0 != null ? depth0.station : depth0)) != null ? stack1.name : stack1), depth0))
    + "</h1>\nBlah";
},"useData":true});
})();
