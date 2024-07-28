from django.urls import path
from .views import UserCreateView, CustomTokenObtainPairView, ExpenseCreateView, UserExpensesView, AllExpensesView, DownloadBalanceSheetView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('expenses/', ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/user/', UserExpensesView.as_view(), name='user_expenses'),
    path('expenses/all/', AllExpensesView.as_view(), name='overall_expenses'),
    path('expenses/balance_sheet/', DownloadBalanceSheetView.as_view(), name='download_balance_sheet'),
    path('user/', UserDetailView.as_view(), name='user_detail')
]