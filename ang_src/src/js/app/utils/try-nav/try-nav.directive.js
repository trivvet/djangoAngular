'use strict';

angular.module('tryNav').
    directive('tryNav', function(Post, $location, $rootScope) {
        return {
            restrict: "E",
            templateUrl: '/templates/nav-bar.html',
            link: function (scope, element, attr) {
                var getElements = []
                scope.getElements = Post.query();
                scope.selectItem = function($item, $model, $label) {
                    $location.path('/blog/' + $item.id); 
                    scope.blogFilter = "";      
                }
                scope.searchItem = function(){
                    $location.path('/blog').search('q', scope.blogFilter);
                    scope.blogFilter = ""; 
                }
            }
        }
    });