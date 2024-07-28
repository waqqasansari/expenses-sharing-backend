from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import generics, status

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()  # Queryset of all User objects
    serializer_class = UserSerializer  # Serializer class for user creation
    permission_classes = [AllowAny]  # Allow any user to access this view

    def perform_create(self, serializer):
        serializer.save()  # Save the new user instance

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
from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # Custom serializer for obtaining JWT token


class ExpenseCreateView(generics.CreateAPIView):
    queryset = Expense.objects.all()  # Queryset of all Expense objects
    serializer_class = ExpenseSerializer  # Serializer class for expense creation
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)  # Save the new expense instance with the user who created it


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Expense, Participant

class UserExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the authenticated user making the request
        user = request.user
        
        # Retrieve all participants where the user is involved
        participants = Participant.objects.filter(user=user)
        
        # Extract expenses associated with each participant
        expenses = [p.expense for p in participants]
        
        # Prepare the response data in a structured format
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
        # Return the structured data as a JSON response
        return Response(data)

class AllExpensesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve all expenses from the database
        expenses = Expense.objects.all()
        
        # Prepare the response data in a structured format
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


class DownloadBalanceSheetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Prepare HTTP response with CSV content type and file name
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

        # Initialize CSV writer and write header row
        writer = csv.writer(response)
        writer.writerow(['Expense', 'User', 'Amount'])

        # Individual expenses for the user
        user = request.user
        participants = Participant.objects.filter(user=user)
        for participant in participants:
            writer.writerow([participant.expense.title, participant.user.email, participant.amount])

        # Add empty row for separation
        writer.writerow([])

        # Write section header for overall expenses
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

# Get the custom User model defined for the project
User = get_user_model()

class UserDetailView(generics.RetrieveAPIView):

    # Queryset containing all User objects
    queryset = User.objects.all()

    # Serializer class responsible for converting User objects to/from JSON
    serializer_class = UserSerializer

    # Permission classes defining who can access this view (authenticated users only)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Retrieve and return the currently authenticated user
        return self.request.user