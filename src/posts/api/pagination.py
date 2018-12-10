from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination
    )

class PostPagePagination(PageNumberPagination):
    page_size = 3