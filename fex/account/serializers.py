from django.contrib.auth.models import Group
from rest_framework import serializers
from account.models import User
from account.permissions import IsOwnerOnly


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
    	model = Group
    	fields = ['name']

class UserSerializer(serializers.ModelSerializer):

	
	groups = GroupSerializer(many=True, read_only=True)
	balance = serializers.IntegerField(default=0, read_only=True)
	freeze_balance = serializers.IntegerField(default=0, read_only=True)
	is_active = serializers.BooleanField(default=True, read_only=True)

	class Meta:
		model = User
		fields = ['url', 'email', 'password', 'first_name', 'last_name', 'groups', 'is_active', 'balance', 'freeze_balance']



class UserSerializer_1(serializers.ModelSerializer):


	class Meta:
		model = User
		fields = ['url']
		print(IsOwnerOnly)
