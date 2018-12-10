from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination
    )

class CommentPagePagination(PageNumberPagination):
    page_size = 2