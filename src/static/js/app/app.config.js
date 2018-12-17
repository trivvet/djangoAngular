'use strict';

angular.module('try').
    config(
        function(
            $locationProvider,
            $resourceProvider,
            $routeProvider
            ){

            $locationProvider.html5Mode({
                enabled: true
            });
            $resourceProvider.defaults.stripTrailingSlashes = false;
            $routeProvider.
                when("/", {
                    template: "<some-list></some-list>"
                }).
                when("/about", {
                    templateUrl: "/api/templates/about.html"
                }).
                when("/blog", {
                    template: "<some-list></some-list>"
                }).
                when("/blog/:id", {
                    template: "<blog-detail></blog-detail>"
                }).
                when("/405", {
                    template: "<h1>There is problems with Data Base</h1>"
                }).
                otherwise({
                    template: "<h1>Not Found</h1>"
                })

        }
    );
