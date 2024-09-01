from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Order, CustomUser
from .serializers import ProductSerializer, CategorySerializer, OrderSerializer, RegisterSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from .permission import IsAdminOrReadOnly

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ IsAdminOrReadOnly]

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