console.log('IMPORTED')
var phonecatApp = angular.module('AdminApp', []);

phonecatApp.controller('ActualController', function PhoneListController($scope) {
    $scope.actual = {
        title: 'Droga krzyżowa',
        content: 'Zapraszamy',
        date: '2017-06-02'
    }

});

phonecatApp.controller('ActionList', function PhoneListController($scope) {
  $scope.serverName = 'http://127.0.0.1:8000/';
  $scope.actions = [
    {
      name: 'Aktualności',
      link: 'actual'
    },
    {
      name: 'Godziny działania kancelari',
      link: 'cancelary'
    }
  ];
});