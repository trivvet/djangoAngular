'use strict';

angular.module('post').
    factory('Post', function($resource){

        var url = '/json/posts.json';

        return $resource(url, {}, {
            query: {
                method: "GET",
                params: {},
                isArray: true,
                cache: true
            },
            get: {
                method: "GET",
                isArray: true,
                cache: true
            }
        });

    });