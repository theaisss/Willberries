from django.core.serializers import serialize

from .pagination import CategoryPagination, ProductPagination
from .serializers import (UserProfileSerializer, CategoryListSerializer, CategoryDetailSerializer,
                          SubCategoryListSerializer, ProductListSerializer, ProductDetailSerializer,
                          SubCategoryDetailSerializer, ReviewSerializer, UserRegisterSerializer,
                          UserLoginSerializer, CartSerializer, CartItemSerializer, FavoriteSerializer,
                          FavoriteItemSerialize)
from .models import (UserProfile, Category, SubCategory,
                     Product,Review, Cart, CartItem, Favorite, FavoriteItem)
from rest_framework import viewsets, generics, permissions, status
from.pagination import ProductPagination,CategoryPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = CategoryPagination


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer



class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryListSerializer


class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price', 'created_date']



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer




class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]



class CartViewSet(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, create = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = FavoriteItem.objects.all()
    serializer_class = FavoriteItemSerialize


# from venv import create
# from yaml import serializer
#
# from .serializers import (UserProfileSerializer, CategoryListSerializer,CategoryDetailSerializer,
#                           SubCategoryListSerializer, SubCategoryDetailSerializer, ReviewSerializer,
#                           ProductListSerializer, ProductDetailSerializer,UserRegisterSerializer, UserLoginSerializer,
#                           CartSerializer, CartItemSerializer,FavoriteSerializer,FavoriteItemSerialize )
#
# from .models import  (UserProfile, Category, SubCategory, Product, ProductImage, Review, Cart,
#                       CartItem, Favorite, FavoriteItem)
# from rest_framework import viewsets, generics,permissions, status
# from .pagination import CategoryPagination, ProductPagination, SubCategoryPagination
# from django_filters.rest_framework import DjangoFilterBackend
# from .filters import ProductFilter, SubCategoryFilter
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.response import Response
# from  rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
#
# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserRegisterSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class LoginView(TokenObtainPairView):
#     serializer_class = UserLoginSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#         except Exception:
#             return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)
#
#         user = serializer.validated_data
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class LogoutView(generics.GenericAPIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             refresh_token = request.data["refresh"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
# class UserProfileViewSet(viewsets.ModelViewSet):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     def get_queryset(self):
#      return UserProfile.objects.filter(id=self.request.user.id)
#
# class CategoryListAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryListSerializer
#     pagination_class = CategoryPagination
#
# class CategoryDetailAPIView(generics.RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategoryDetailSerializer
#
# class SubCategoryListAPIView(generics.ListAPIView):
#     queryset = SubCategory.objects.all()
#     serializer_class = SubCategoryListSerializer
#     pagination_class = SubCategoryPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = SubCategoryFilter
#
# class SubCategoryDetailAPIView(generics.RetrieveAPIView):
#     queryset = SubCategory.objects.all()
#     serializer_class = SubCategoryDetailSerializer
#
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
#     pagination_class = ProductPagination
#     filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
#     filterset_class = ProductFilter
#     search_fields = ['product_name', 'article_number']
#     ordering_fields = ['price','created_date']
#
# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailSerializer
#
#
# class  ReviewViewSet(viewsets.ModelViewSet):
#     queryset =  Review.objects.all()
#     serializer_class =  ReviewSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
#
# class CartViewSet(generics.RetrieveAPIView):
#     serializer_class = CartSerializer
#
#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)
#
#     def retrieve(self, request, *args, **kwargs):
#         cart, created = Cart.objects.get_or_create(user = request.user)
#         serializer = self.get_serializer(cart)
#         return Response(serializer.data)
#
#
#
# class CartItemViewSet(viewsets.ModelViewSet):
#     serializer_class = CartItemSerializer
#
#     def get_queryset(self):
#         return CartItem.objects.filter(cart_user=self.request.user)
#
#     def perform_create(self, serializer):
#         cart, created = Cart.objects.get_or_create(user=self.request.user)
#         serializer.save(cart=cart)
#
#
# class FavoriteViewSet(viewsets.ModelViewSet):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoriteSerializer
#
#
# class FavoriteItemViewSet(viewsets.ModelViewSet):
#     queryset = FavoriteItem.objects.all()
#     serializer_class = FavoriteItemSerialize
#
#
#
# # from .serializers import (
# #     UserProfileSerializer, CategoryListSerializer, CategoryDetailSerializer,
# #     SubCategoryListSerializer, ProductListSerializer, ProductDetailSerializer,
# #     SubCategoryDetailSerializer, ReviewSerializer
# # )
# # from .models import (
# #     UserProfile, Category, SubCategory,
# #     Product, Review
# # )
# # from rest_framework import viewsets, generics
# #
# #
# # class UserProfileViewSet(viewsets.ModelViewSet):
# #     queryset = UserProfile.objects.all()
# #     serializer_class = UserProfileSerializer
# #
# #
# # class CategoryListAPIView(generics.ListAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategoryListSerializer
# #
# #
# # class CategoryDetailAPIView(generics.RetrieveAPIView):
# #     queryset = Category.objects.all()
# #     serializer_class = CategoryDetailSerializer
# #
# #
# # class SubCategoryListAPIView(generics.ListAPIView):
# #     queryset = SubCategory.objects.all()
# #     serializer_class = SubCategoryListSerializer
# #
# #
# # class SubCategoryDetailAPIView(generics.RetrieveAPIView):
# #     queryset = SubCategory.objects.all()
# #     serializer_class = SubCategoryDetailSerializer
# #
# #
# # class ProductListAPIView(generics.ListAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductListSerializer
# #
# #
# # class ProductDetailAPIView(generics.RetrieveAPIView):
# #     queryset = Product.objects.all()
# #     serializer_class = ProductDetailSerializer
# #
# #
# #
# # class ReviewViewSet(viewsets.ModelViewSet):
# #     queryset = Review.objects.all()
# #     serializer_class = ReviewSerializer
# #
# #
# #
# # # from rest_framework import viewsets
# # # from .models import (
# # #     UserProfile, Category, SubCategory, Product,
# # #     ProductImage, Review
# # #
# # # )
# # # from.serializers import (
# # #     UserProfileSerializer, CategorySerializer, SubCategorySerializer,
# # #     ProductSerializer, ProductImageSerializer, ReviewSerializer,
# # # )
# # #
# # # class UserProfileViewSet(viewsets.ModelViewSet):
# # #     queryset = UserProfile.objects.all()
# # #     serializer_class = UserProfileSerializer
# # #
# # #
# # # class CategoryViewSet(viewsets.ModelViewSet):
# # #     queryset = Category.objects.all()
# # #     serializer_class = CategorySerializer
# # #
# # # class SubCategoryViewSet(viewsets.ModelViewSet):
# # #     queryset = SubCategory.objects.all()
# # #     serializer_class = SubCategorySerializer
# # #
# # #
# # # class ProductViewSet(viewsets.ModelViewSet):
# # #     queryset = Product.objects.all()
# # #     serializer_class = ProductSerializer
# # #
# # # class ProductImageViewSet(viewsets.ModelViewSet):
# # #     queryset = ProductImage.objects.all()
# # #     serializer_class = ProductImageSerializer
# # #
# # # class ReviewViewSet(viewsets.ModelViewSet):
# # #     queryset = Review.objects.all()
# # #     serializer_class = ReviewSerializer