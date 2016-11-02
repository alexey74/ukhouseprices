'use strict';

angular
    .module('ukHousePricesApp')
    .controller('pricePaidCtrl', function($scope, $http, $filter) {
        $scope.getTown = function(term) {
            return $http.get('/api/town?search=' + term).then(function(data) {
                //console.debug('res=' + angular.toJson(data.data.results));
                return data.data.results;
            });
        };
        $scope.submit = function() {
            console.debug('town=' + angular.toJson($scope.selectedTown));
            console.debug('sd=' + angular.toJson($scope.start_date));
            console.debug('ed=' + angular.toJson($scope.end_date));
            var url = '/api/pricepaidstats?town=' + $scope.selectedTown.id;
            var DF='yyyy-MM-dd';
            
            if ($scope.start_date) {
                url += '&transfer_date_0=' + $filter('date')($scope.start_date, DF);
            }
            if ($scope.end_date) {
                url += '&transfer_date_1=' + $filter('date')($scope.end_date, DF);
            }
            console.debug('url=' + url);
            return $http.get(url).success(function(data) {
                console.debug('res=' + angular.toJson(data.results));
                $scope.result = data.results;
            });
        };
        
        $scope.order = function(predicate) {
            var orderBy = $filter('orderBy');
            $scope.predicate = predicate;
            $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
            $scope.result = orderBy($scope.result, predicate, $scope.reverse);
          };        
    });
