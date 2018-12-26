'use strict';

angular.module('blogDetail').
    component('blogDetail', {
        templateUrl: '/api/templates/blog-detail.html',
        controller: function(
            Post, 
            $cookies, 
            $http,
            $location, 
            $routeParams, 
            $scope
            ) {
            var slug = $routeParams.slug;
            var token = $cookies.get("token");
            Post.get({'slug': slug}, function(data) {   
                $scope.post = data;
                $scope.notFound = false;
                checkCommentsLength($scope.post.comments);
            });

            $scope.addReply = function() {
                if (token) {
                    var reqConfig = {
                        method: "POST",
                        url: "http://localhost:8000/api/comments/create/?slug=" + slug + "&type=post",
                        data: {
                            content: $scope.reply.content
                        },
                        headers: {
                            authorization: "JWT " + token
                        }
                    } 
                    var requestAction = $http(reqConfig);
                    requestAction.success(
                        function(r_data, r_status, r_headers, r_config) {
                            if ($scope.comments) {
                                $scope.comments.push($scope.reply);
                            } else {
                                $scope.comments = [$scope.reply, ];
                            }
                            resetReply($scope.comments);
                         });

                    requestAction.error(
                        function(e_data, e_status, e_headers, e_config) {
                           console.log(e_data); 
                        });
                    
                } else {
                    console.log("No token");
                }
                
            }

            $scope.deleteReply = function(comment) {
                $scope.$apply(
                    $scope.comments.splice(comment, 1),
                    checkCommentsLength($scope.comments)
                );
                
            }

            function checkCommentsLength(comments) {
                if (comments && comments.length > 0) {
                    $scope.commentsExist = true;
                    $scope.comments = comments;
                } else {
                    $scope.commentsExist = false;
                }
            }

            function resetReply(comments) {
                var length = 0;
                if (comments) {
                    length = comments.length + 1;
                } else {
                    length = 1;
                }
                $scope.commentsExist = true;
                $scope.reply = {
                    "content": ""
                }
            }

            if ($scope.notFound) {
                $location.path("/404");
            }

        }
    });