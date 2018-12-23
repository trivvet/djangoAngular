'use strict';

angular.module('try', [
    // external
    'ngResource',
    'ngRoute',
    'angularUtils.directives.dirPagination',
    'ui.bootstrap',
    'ngCookies',

    // internal
    'blogList',
    'blogDetail',
    'loginDetail',
    'confirmClick',
    'tryNav'
]);