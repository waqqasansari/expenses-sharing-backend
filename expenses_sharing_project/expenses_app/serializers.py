from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'mobile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile=validated_data['mobile']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            print(email,'-----' ,password)
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token



from rest_framework import serializers
from .models import Expense, Participant
from django.contrib.auth import get_user_model

User = get_user_model()

class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_name = serializers.CharField(source='user.name', read_only=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)

    class Meta:
        model = Participant
        fields = ['user', 'user_name', 'amount', 'percentage']

# class ExpenseSerializer(serializers.ModelSerializer):
#     participants = ParticipantSerializer(many=True)

#     class Meta:
#         model = Expense
#         fields = ['id', 'title', 'amount', 'split_method', 'created_by', 'participants']
    
#     def create(self, validated_data):
#         participants_data = validated_data.pop('participants')
#         expense = Expense.objects.create(**validated_data)

#         if expense.split_method == 'equal':
#             split_amount = expense.amount / len(participants_data)
#             for participant_data in participants_data:
#                 Participant.objects.create(expense=expense, user=participant_data['user'], amount=split_amount)
        
#         elif expense.split_method == 'exact':
#             for participant_data in participants_data:
#                 Participant.objects.create(expense=expense, user=participant_data['user'], amount=participant_data['amount'])
        
#         elif expense.split_method == 'percentage':
#             for participant_data in participants_data:
#                 split_amount = expense.amount * (participant_data['percentage'] / 100)
#                 Participant.objects.create(expense=expense, user=participant_data['user'], amount=split_amount, percentage=participant_data['percentage'])

#         return expense


class ExpenseSerializer(serializers.ModelSerializer):
    # Serializer for nested 'participants' field
    participants = ParticipantSerializer(many=True)
    # Primary key related field for 'created_by' user
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # Read-only field to display 'created_by' user's name
    created_by_name = serializers.CharField(source='created_by.name', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'split_method', 'created_by', 'created_by_name', 'participants']

    def validate(self, data):
        # Validate the data based on the chosen 'split_method'
        split_method = data.get('split_method')
        participants = data.get('participants', [])
        
        if split_method == 'equal':
            # Validate 'equal' split method
            if len(participants) == 0:
                raise serializers.ValidationError("At least one participant is required.")
            split_amount = data['amount'] / len(participants)
            for participant in participants:
                participant['amount'] = split_amount
                participant['percentage'] = None
        
        elif split_method == 'exact':
            # Validate 'exact' split method
            total_amount = sum(participant.get('amount', 0) for participant in participants)
            if total_amount != data['amount']:
                raise serializers.ValidationError("The sum of exact amounts must equal the total amount.")
            for participant in participants:
                participant['percentage'] = None

        elif split_method == 'percentage':
            # Validate 'percentage' split method
            total_percentage = sum(participant.get('percentage', 0) for participant in participants)
            if total_percentage != 100:
                raise serializers.ValidationError("The sum of percentages must equal 100%.")
            for participant in participants:
                participant['amount'] = data['amount'] * (participant['percentage'] / 100)

        else:
            raise serializers.ValidationError("Invalid split method.")
        
        return data

    def create(self, validated_data):
        # Create Expense instance and associated Participants
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            Participant.objects.create(expense=expense, **participant_data)
        return expense