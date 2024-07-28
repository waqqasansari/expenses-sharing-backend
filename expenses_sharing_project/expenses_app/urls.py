from django.urls import path
from .views import (
    UserCreateView, 
    CustomTokenObtainPairView, 
    ExpenseCreateView, 
    UserExpensesView, 
    AllExpensesView, 
    DownloadBalanceSheetView, 
    UserDetailView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),  # Endpoint for user registration
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint for user login and obtaining JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint for refreshing JWT token
    path('expenses/', ExpenseCreateView.as_view(), name='expense_create'),  # Endpoint for creating an expense
    path('expenses/user/', UserExpensesView.as_view(), name='user_expenses'),  # Endpoint for retrieving individual user expenses
    path('expenses/all/', AllExpensesView.as_view(), name='overall_expenses'),  # Endpoint for retrieving overall expenses for all users
    path('expenses/balance_sheet/', DownloadBalanceSheetView.as_view(), name='download_balance_sheet'),  # Endpoint for downloading the balance sheet
    path('user/', UserDetailView.as_view(), name='user_detail')  # Endpoint for retrieving user details
]