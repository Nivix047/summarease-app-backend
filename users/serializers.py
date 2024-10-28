from rest_framework import serializers
from .models import CustomUser
from pdfs.serializers import PDFDocumentSerializer
from django.contrib.auth.password_validation import validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    pdf_documents = PDFDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_instance = CustomUser(**validated_data)
        user_instance.set_password(password)
        user_instance.save()
        return user_instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
