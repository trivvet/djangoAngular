'use strict';

angular.module('try', [
    // external
    'ngResource',
    'ngRoute',
    'angularUtils.directives.dirPagination',
    'ui.bootstrap',

    // internal
    'blogList',
    'blogDetail',
    'confirmClick',
    'tryNav'
]);