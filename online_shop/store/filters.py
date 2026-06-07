from django_filters import FilterSet
from .models import Product, SubCategory

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
        'subcategory':['exact'],
        'product_type':['exact'],
        'article_number':['exact'],
        'price':['gt','lt']

        }
class SubCategoryFilter(FilterSet):
    class Meta:
        model = SubCategory
        fields = {
        'category':['exact']
        }