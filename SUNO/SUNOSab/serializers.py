from rest_framework import serializers
from SUNOSab.models import Register

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ('UserID',
                  'Username',
                  'Email',
                  'Password')