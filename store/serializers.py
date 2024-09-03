from rest_framework import serializers # type: ignore
from .models import Product, Category, Order, OrderItem, CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'fullname', 'phone', 'address', 'role')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'fullname')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False} 
        }

    def create(self, validated_data):
        username = validated_data.get('username', validated_data['email'])

        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data.get('fullname', '')
        )
        return user

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    total_products = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'description', 'total_products']

# Product Serializer
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = '__all__'

# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = ['product', 'product_details', 'quantity']
    
    def get_product_details(self, obj):
        product = obj.product
        return {
            "name": product.name,
            "img": product.img,
            "price": product.price,
            "category_name": product.category.name
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('product', None)
        return representation

# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True)
    phone = serializers.CharField(write_only=True, required=False)  # Add phone field
    address = serializers.CharField(write_only=True, required=False)  # Add address field

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')  # Extract items data
        phone = validated_data.pop('phone', None)  # Extract phone data
        address = validated_data.pop('address', None)  # Extract address data
        
        # Remove user from validated_data if present
        if 'user' in validated_data:
            validated_data.pop('user')

        user = self.context['request'].user  # Get the user from the request context

        # Update user's phone and address if not set
        if phone and not user.phone:
            user.phone = phone
        if address and not user.address:
            user.address = address
        user.save()

        # Create the order with the provided user
        order = Order.objects.create(user=user, **validated_data)

        # Create each order item associated with the order
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
    