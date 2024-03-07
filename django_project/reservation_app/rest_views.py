from django.shortcuts import get_object_or_404
from rest_framework import status, filters, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .rest_models import Rest_Customer, Rest_Reservation, Rest_IHA
from .serializers import CustomerRegisterSerializer, IHASerializer, CustomerSerializer, CustomerLoginSerializer, ReservationSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import permissions

class IHAViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Rest_IHA.objects.all()
        serializer = IHASerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = IHASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        serializer = IHASerializer(iha)
        return Response(serializer.data)

    def update(self, request, pk=None):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        serializer = IHASerializer(iha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        serializer = IHASerializer(iha, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        iha.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "User logged in successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = Rest_Customer.objects.all()
        serializer = CustomerSerializer(users, many=True)
        return Response(serializer.data)

class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = Rest_Customer.objects.get(pk=pk)
        except Rest_Customer.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(user)
        return Response(serializer.data)

class CustomerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user = Rest_Customer.objects.get(pk=pk)
        except Rest_Customer.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            user = Rest_Customer.objects.get(pk=pk)
            user.delete()
            return Response({"message": "User deleted successfully."})
        except Rest_Customer.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class CreateReservationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ReservationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        reservations = Rest_Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Rest_Reservation, pk=pk)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Rest_Reservation, pk=pk)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        reservation = get_object_or_404(Rest_Reservation, pk=pk)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        customers = Rest_Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Rest_Customer, pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Rest_Customer, pk=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        customer = get_object_or_404(Rest_Customer, pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class IHAListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        ihalar = Rest_IHA.objects.all()
        serializer = IHASerializer(ihalar, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = IHASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IHARetrieveUpdateDestroyView(APIView):
    def get(self, request, pk, *args, **kwargs):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        serializer = IHASerializer(iha)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        serializer = IHASerializer(iha, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        iha = get_object_or_404(Rest_IHA, pk=pk)
        iha.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
