from rest_framework.pagination import PageNumberPagination

class CategoryPagination(PageNumberPagination):
    page_size = 5

class ProductPagination(PageNumberPagination):
    page_size = 4

class SubCategoryPagination(ProductPagination):
    page_size = 4