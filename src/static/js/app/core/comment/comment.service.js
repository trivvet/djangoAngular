'use strict';

angular.module('core.comment').
    factory('Comment', function($cookies, $resource){

        var url = '/api/comments/';
        var token = $cookies.get("token");
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
        
        var commentSave = {
            url: url + "create/",
            method: "POST",
            params: {},
        }

        var commentUpdate = {
            url: url + ":id/",
            method: "PUT",
            params: {'id': "@id"},
        }

        var commentDelete = {
            url: url + ":id/",
            method: "DELETE",
            params: {'id': "@id"}
        }

        if (token) {
            commentSave['headers'] = {authorization: "JWT " + token};
            commentUpdate['headers'] = {authorization: "JWT " + token};
            commentDelete['headers'] = {authorization: "JWT " + token};
        } else {
            console.log("No token");
        }

        return $resource(url, {}, {
            query: commentQuery,
            get: commentGet,
            save: commentSave,
            update: commentUpdate,
            delete: commentDelete
        });

    });