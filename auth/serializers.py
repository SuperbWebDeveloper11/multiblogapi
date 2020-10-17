from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator



class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, required=True,
        help_text='enter your password',
        style={'input_type': 'password', 'placeholder': 'password'}
    )
        
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'groups']
        
        def create(self, validated_data):                                       
            user = User(                                                        
                    email=validated_data['email'],                              
                    username=validated_data['username']                         
                    )                                                                                                      
            user.set_password(validated_data['password'])                       
            # i got this in admin site
            # Invalid password format or unknown hashing algorithm
            user.save()                                                         
            return user 


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


