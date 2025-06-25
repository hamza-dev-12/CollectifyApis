from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group, Member, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObatainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)
        self.fields["email"] = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("No account found with this email.")

            # Check if password is correct
            if not user.check_password(password):
                raise serializers.ValidationError("Incorrect password.")

            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            # Set username for token generation
            attrs["username"] = user.username

            # Remove email from attrs since parent expects username
            attrs.pop("email")

        data = super().validate(attrs)
        data["user_id"] = self.user.id

        return data


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "password": {"required": True, "write_only": True},
        }

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "group_name", "base_amount", "admin"]
        extra_kwargs = {
            "group_name": {"required": True},
            "admin": {"required": True},
            "base_amount": {"required": True},
        }


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ["id", "group", "member_name", "email"]
        extra_kwargs = {
            "group": {"required": False, "read_only": True},
            # "id": {"required": True},
            "member_name": {"required": True},
            "email": {"required": True},
        }


class PaymentSerializer(serializers.ModelSerializer):
    group_members = MemberSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ("id", "date", "amount", "status", "group_members")

        extra_kwargs = {
            "date": {"required": True},
            "amount": {"required": True},
            "status": {"required": False},
            # "group_members": {"required": False},
            # "group_and_members": {"required": False},
        }
