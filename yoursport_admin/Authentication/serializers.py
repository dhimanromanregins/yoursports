from rest_framework import serializers
from .models import (CustomUser, Pricing, Contact,PasswordResetToken,
                     FootballTeam,PlayerDetail, FAQ, EndUserDetail, EndUser)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'full_name', 'institution', 'address', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ('id', 'amount', 'description', 'gerneral', 'school_corporate')


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def validate_fullname(self, value):
        if not value:
            raise serializers.ValidationError("Full name is required.")
        return value

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_subject(self, value):
        if not value:
            raise serializers.ValidationError("Subject is required.")
        return value

    def validate_message(self, value):
        if not value:
            raise serializers.ValidationError("Message is required.")
        if len(value) < 100:
            raise serializers.ValidationError("Message must be at least 100 characters long.")
        return value

class PasswordResetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = '__all__'


class FootballTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = FootballTeam
        fields = '__all__'

    def validate(self, data):
        errors = {}

        # Check if required fields are provided
        required_fields = ['name', 'city', 'founded_year', 'coach', 'captain']
        for field in required_fields:
            if field not in data or data[field] == '':
                errors[field] = ['This field is required.']

        # If there are any errors, raise validation error
        if errors:
            raise serializers.ValidationError(errors)

        return data


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'institution', 'address']


class PlayerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerDetail
        fields = ['id', 'name', 'position', 'football_team']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']


class EndUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUser
        fields = '__all__'

class EndUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserDetail
        fields = '__all__'