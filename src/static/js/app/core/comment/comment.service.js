'use strict';

angular.module('core.comment').
    factory('Comment', function($resource){

        var url = '/api/comments/';
        var commentQuery = {
            url: url,
            method: "GET",
            params: {},
            isArray: true,
            cache: false,
            transformResponse: function (data) {
                return angular.fromJson(data).results;
            }
        }

        var commentGet = {
            url: url + ":id",
            method: "GET",
            params: {"id": "@id"},
            isArray: true,
            cache: true,
            transformResponse: function (data) {
                return angular.fromJson(data).results;
            }
        }

        return $resource(url, {}, {
            query: commentQuery,
            get: commentGet
        });

    });