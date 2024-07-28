from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import generics, status

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User Created Successfully. Now perform Login to get your token"})
#         else:
#             errors = serializer.errors
#             error_message = {}
#             for field, error_list in errors.items():
#                 error_message[field] = [str(error) for error in error_list]
#             return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)

# from django.db import transaction

# class UserCreateView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         # Get data from request
#         email = request.data.get('email')
#         mobile = request.data.get('mobile')
#         password = request.data.get('password')

#         # Normalize email
#         normalized_email = email.lower()

#         # Check if email or mobile already exist
#         if User.objects.filter(email=normalized_email).exists():
#             return Response({"message": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(mobile=mobile).exists():
#             return Response({"message": "Mobile number already registered"}, status=status.HTTP_400_BAD_REQUEST)

#         # Perform additional password validation
#         if len(password) < 6:
#             return Response({"message": "Password must be at least 6 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        
#         # You can add more password complexity checks here

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             serialized_user = UserSerializer(user).data  # Serialize the user object
#             return Response({
#                 "message": "User Created Successfully. Now perform Login to get your token",
#                 "user": serialized_user
#             })
#         else:
#             errors = serializer.errors
#             error_message = {}
#             for field, error_list in errors.items():
#                 error_message[field] = [str(error) for error in error_list]
#             return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
        


from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated

class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# class UserExpensesView(generics.ListAPIView):
#     serializer_class = ExpenseSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Expense.objects.filter(participants__user=self.request.user)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Participant

class UserExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        participants = Participant.objects.filter(user=user)
        expenses = [p.expense for p in participants]
        data = [
            {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "split_method": expense.split_method,
                "created_by": expense.created_by.id,
                "participants": [
                    {"user": participant.user.id, "amount": participant.amount}
                    for participant in expense.participants.all()
                ]
            }
            for expense in expenses
        ]
        return Response(data)

# class OverallExpensesView(generics.ListAPIView):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer
#     permission_classes = [permissions.IsAuthenticated]

class AllExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        expenses = Expense.objects.all()
        data = [
            {
                "id": expense.id,
                "title": expense.title,
                "amount": expense.amount,
                "split_method": expense.split_method,
                "created_by": expense.created_by.id,
                "participants": [
                    {"user": participant.user.id, "amount": participant.amount}
                    for participant in expense.participants.all()
                ]
            }
            for expense in expenses
        ]
        return Response(data)


import csv
from django.http import HttpResponse
from .models import Participant

# class DownloadBalanceSheetView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

#         writer = csv.writer(response)
#         writer.writerow(['Expense', 'User', 'Amount'])

#         participants = Participant.objects.filter(user=request.user)
#         for participant in participants:
#             writer.writerow([participant.expense.title, participant.user.email, participant.amount])

#         return response


class DownloadBalanceSheetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

        writer = csv.writer(response)
        writer.writerow(['Expense', 'User', 'Amount'])

        # Individual expenses for the user
        user = request.user
        participants = Participant.objects.filter(user=user)
        for participant in participants:
            writer.writerow([participant.expense.title, participant.user.email, participant.amount])

        writer.writerow([])
        writer.writerow(['Overall Expenses'])
        writer.writerow(['Expense', 'User', 'Amount'])

        # Overall expenses for all users
        participants = Participant.objects.all()
        for participant in participants:
            writer.writerow([participant.expense.title, participant.user.email, participant.amount])

        return response


from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer

User = get_user_model()

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user