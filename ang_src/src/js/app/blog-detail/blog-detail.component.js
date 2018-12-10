'use strict';

angular.module('blogDetail').
    component('blogDetail', {
        templateUrl: '/templates/blog-detail.html',
        controller: function(Post, $location, $routeParams, $scope) {
            
            Post.query(function(data){
                $scope.notFound = true;
                data.forEach(function(post) {
                    if (post.id == $routeParams.id) {
                        $scope.post = post;
                        $scope.notFound = false;
                        checkCommentsLength($scope.post.comments);
                    }
                });
            });

            $scope.addReply = function() {
                if ($scope.post.comments) {
                    $scope.post.comments.push($scope.reply);
                } else {
                    $scope.post.comments = [$scope.reply, ];
                }
                resetReply($scope.post);
            }

            $scope.deleteReply = function(comment) {
                $scope.$apply(
                    $scope.post.comments.splice(comment, 1),
                    checkCommentsLength($scope.post.comments)
                );
                
            }

            function checkCommentsLength(comments) {
                if (comments && comments.length > 0) {
                    $scope.commentsExist = true;
                } else {
                    $scope.commentsExist = false;
                }
            }

            function resetReply(post) {
                var length = 0;
                if (post.comments) {
                    length = post.comments.length + 1;
                } else {
                    length = 1;
                }
                $scope.commentsExist = true;
                $scope.reply = {
                    "id": length,
                    "text": ""
                }
            }

            if ($scope.notFound) {
                $location.path("/404");
            }

        }
    });