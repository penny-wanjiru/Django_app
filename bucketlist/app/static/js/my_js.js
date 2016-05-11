$(document).ready(function(){
// the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
$('.modal-trigger').leanModal();
});


var myApp = angular.module('myApp', []);
myApp.controller('mainCtrl', function Main($scope, $http){
  
  $http.get('http://api.randomuser.me/?results=24').success(function(data) {
    $scope.users = data.results;
  }).error(function(data, status) {
    alert('get data error!');
  });
});

