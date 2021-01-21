from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from account.serializers import UserSerializer
from account.models import User
from account.permissions import IsOwnerOnly


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = UserSerializer

	def get_queryset(self):

		if self.request.user.is_authenticated and not self.request.user.is_superuser:
			queryset = User.objects.filter(email=self.request.user.email)
		else:
			queryset = User.objects.all().order_by('-date_joined')
		return queryset
	
	def get_permissions(self):

		if self.request.method == 'GET':
			self.permission_classes = [permissions.IsAuthenticated & (IsOwnerOnly | permissions.IsAdminUser), ]
		else:
			self.permission_classes = [IsOwnerOnly | permissions.IsAdminUser, ]
		return super(UserViewSet, self).get_permissions()
