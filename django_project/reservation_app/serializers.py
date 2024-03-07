from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .rest_models import Rest_IHA, Rest_Customer, Rest_Reservation

# We define a serializer for the IHA model. This serializer contains all fields of the IHA model.
class IHASerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_IHA
        fields = '__all__'

# We define a ViewSet for the IHA model. This ViewSet allows us to manage operations related to IHAs via REST API.
class IHAViewSet(viewsets.ViewSet):
# We specify that users must be authorized to access this ViewSet.
    permission_classes = [IsAuthenticated]

    # Lists all IHAs.
    def list(self, request):
        queryset = Rest_IHA.objects.all()
        serializer = IHASerializer(queryset, many=True)
        return Response(serializer.data)

    # Creates a new IHA.
    def create(self, request):
        serializer = IHASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Brings up a specific IHA.
    def retrieve(self, request, pk=None):
        queryset = Rest_IHA.objects.all()
        iha = get_object_or_404(queryset, pk=pk)
        serializer = IHASerializer(iha)
        return Response(serializer.data)

    # Updates a specific IHA.
    def update(self, request, pk=None):
        iha = Rest_IHA.objects.get(pk=pk)
        serializer = IHASerializer(iha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Partially updates a given IHA.
    def partial_update(self, request, pk=None):
        iha = Rest_IHA.objects.get(pk=pk)
        serializer = IHASerializer(iha, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Deletes a specific IHA.
    def destroy(self, request, pk=None):
        iha = Rest_IHA.objects.get(pk=pk)
        iha.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# We define a serializer for the customer model. This serializer will be used during customer registration and update.
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_Customer
        fields = ['id', 'email', 'username', 'name', 'surname', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Parola alanını sadece yazılabilir yapar, okunamaz.

    # It allows hashing of the password when creating a new customer.
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # Ensures the password is hashed correctly when updating the client.
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

# Serializer to be used for customer registration. It includes username, email, first name, last name and password.
class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_Customer
        fields = ('email', 'username', 'name', 'surname', 'password')
        extra_kwargs = {'password': {'write_only': True}}  # Makes the password field writable only.

    # Creates a new customer. In the meantime, the password is hashed.
    def create(self, validated_data):
        user = Rest_Customer.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            surname=validated_data['surname']
        )
        return user

# Serializer to be used for customer login. Contains username and password.
class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    # It allows user authentication with username and password.
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

# Serializer to be used for booking creation. Includes customer, IHA, start and end dates.
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_Reservation
        fields = ['customer', 'iha', 'number', 'start_date', 'finish_date', 'total_price']
        read_only_fields = ['total_price']  # The total price field is calculated automatically, it cannot be entered manually.

    # Creates a new reservation. The total price is calculated based on the number of days between the start and end dates and the price of the IHA.
    def create(self, validated_data):
        iha = validated_data['iha']
        iha_price = iha.price

        start_date = validated_data['start_date']
        finish_date = validated_data['finish_date']
        day_count = (finish_date - start_date).days

        total_price = day_count * iha_price
        validated_data['total_price'] = total_price

        reservation = Rest_Reservation.objects.create(**validated_data)

        return reservation
