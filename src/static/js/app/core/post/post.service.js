'use strict';

angular.module('post').
    factory('Post', function($resource){

        var url = '/api/posts/:slug/';

        return $resource(url, {}, {
            query: {
                method: "GET",
                params: {},
                isArray: true,
                cache: true,
                transformResponse: function (data) {
                    return angular.fromJson(data).results;
                }
            },
            get: {
                method: "GET",
                params: {'slug': '@slug'},
                isArray: false,
                cache: false
            }
        });

    });