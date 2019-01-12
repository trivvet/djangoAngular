'use strict';

angular.module('blogDetail').
    component('blogDetail', {
        templateUrl: '/api/templates/blog-detail.html',
        controller: function(
            Post, 
            Comment,
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
                Comment.query({"slug": slug, "type": "post"}, 
                    function(commentData) {
                    checkCommentsLength(commentData);
                })
            });
            

            $scope.addReply = function() {
                Comment.save(
                    {
                        content: $scope.reply.content,
                        model_type: "post",
                        slug: slug
                    }, function(data) {
                        if ($scope.comments) {
                            $scope.comments.push(data);
                        } else {
                            $scope.comments = [data, ];
                        }
                        resetReply($scope.comments);
                    }, function(e_data) {
                        console.log(e_data);
                    }
                )
            }

            $scope.deleteReply = function(comment) {
                Comment.delete({'id': comment.id},
                    function(data){
                        console.log(data);
                        var index = $scope.comments.indexOf(comment);
                        $scope.comments.splice(index, 1),
                        checkCommentsLength($scope.comments)
                    }, function(e_data) {
                        console.log(e_data)
                    });
                
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