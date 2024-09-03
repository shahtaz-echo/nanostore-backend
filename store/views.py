from rest_framework import viewsets # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from .models import Product, Category, Order, CustomUser
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, RegisterSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from rest_framework import generics # type: ignore
from .permission import IsAdminOrReadOnly
from django.db.models import Count

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(total_products=Count('products'))
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by 'featured' parameter
        featured = self.request.query_params.get('featured')
        if featured is not None:
            is_featured = featured.lower() in ['true', '1', 'yes']
            queryset = queryset.filter(featured=is_featured)

        # Filter by 'category' parameter
        category_id = self.request.query_params.get('category')
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)

        # Filter by 'search' parameter
        search_str = self.request.query_params.get('search')
        if search_str:
            queryset = queryset.filter(name__icontains=search_str)

        return queryset



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return generics.get_object_or_404(CustomUser, id=user_id)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)