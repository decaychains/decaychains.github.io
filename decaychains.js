(function() {

  
  var app = angular.module('decaychains');

  
  
  //Page header
  app.directive('header', function() {
    return {
      restrict: 'E',
      templateUrl: 'header.html',
      controller: 'init'
    };
  });
    
    
})();
