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

            $scope.showReply = function(comment) {
                if (comment.show_reply) {
                    comment.show_reply = false;
                } else {
                    comment.show_reply = true;
                }
                
            }
            $scope.addCommentReply = function(reply, parentComment) {
                Comment.save(
                    {
                        content: reply.content,
                        model_type: "post",
                        slug: slug,
                        parent_id: parentComment.id
                    }, function(data) {
                        parentComment.reply_count += 1;
                        reply.content = "";
                    }, function(e_data) {
                        console.log(e_data);
                    }
                );

            }

            $scope.addNewComment = function() {
                Comment.save(
                    {
                        content: $scope.newComment.content,
                        model_type: "post",
                        slug: slug
                    }, function(data) {
                        if ($scope.comments) {
                            $scope.comments.unshift(data);
                        } else {
                            $scope.comments = [data, ];
                        }
                        resetNewComment($scope.comments);
                    }, function(e_data) {
                        console.log(e_data);
                    }
                )
            }

            $scope.updateReply = function(comment) {
                comment.$update(
                    {
                        id: comment.id,
                        content: $scope.reply.content,
                        model_type: "post",
                        slug: slug
                    }, function(data) {
                    }, function(e_data) {
                        console.log(e_data);
                    }
                )
            }

            $scope.deleteReply = function(comment) {
                comment.$delete({'id': comment.id},
                    function(data){
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

            function resetNewComment(comments) {
                $scope.commentsExist = true;
                $scope.newComment = {
                    "content": ""
                }
            }

            if ($scope.notFound) {
                $location.path("/404");
            }

        }
    });