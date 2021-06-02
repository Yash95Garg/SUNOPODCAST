from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
            },
            'username':{
                'required':True
            },
            'email':{
                'required':True
            },
            'password':{
                'required':True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


