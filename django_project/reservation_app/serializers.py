from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .rest_models import Rest_IHA, Rest_Customer, Rest_Reservation


class IHASerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_IHA
        fields = '__all__'

class IHAViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated] 

    def list(self, request):
        queryset = Rest_IHA.objects.all()
        serializer = IHASerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = IHASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Rest_IHA.objects.all()
        iha = get_object_or_404(queryset, pk=pk)
        serializer = IHASerializer(iha)
        return Response(serializer.data)

    def update(self, request, pk=None):
        iha = Rest_IHA.objects.get(pk=pk)
        serializer = IHASerializer(iha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        iha = Rest_IHA.objects.get(pk=pk)
        serializer = IHASerializer(iha, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        iha = Rest_IHA.objects.get(pk=pk)
        iha.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_Customer
        fields = ['id', 'email', 'username', 'name', 'surname', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Müşteri kayıt işlemi sırasında parolanın doğru bir şekilde hashlenmesi için
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Kullanıcı güncellemesi sırasında parolanın hashlenmesi
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_Customer
        fields = ('email', 'username', 'name', 'surname', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Rest_Customer.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            name=validated_data['name'],
            surname=validated_data['surname']
        )
        return user

class CustomerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rest_Reservation
        fields = ['customer', 'iha', 'number', 'start_date', 'finish_date', 'total_price']
        read_only_fields = ['total_price'] 

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