from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from account.serializers import UserSerializer
from account.models import User
from account.permissions import IsOwnerOnly, IsAnonimousUser
#from django.http import Http404
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""	
	#permission_classes = [IsOwnerOnly | permissions.IsAdminUser]#, permissions.IsAuthenticated]
	#queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

	def get_queryset(self):

		if self.request.user.is_authenticated and not self.request.user.is_superuser:
			queryset = User.objects.filter(email=self.request.user.email)
		else:
			queryset = User.objects.all().order_by('-date_joined')
#		
#		if self.request.user.is_superuser:
#			queryset = User.objects.all().order_by('-date_joined')
#		elif not self.request.user.is_authenticated:
#			queryset = []
#		else:
#			queryset = User.objects.filter(email=self.request.user.email)
		return queryset
	
	def get_permissions(self):

		if self.request.method == 'GET':
			self.permission_classes = [permissions.IsAuthenticated & (IsOwnerOnly | permissions.IsAdminUser), ]
		else:
			self.permission_classes = [IsOwnerOnly | permissions.IsAdminUser, ]
		return super(UserViewSet, self).get_permissions()
        #		if self.action == 'list':
#			permission_classes = [permissions.IsAdminUser]
#		else:
#			permission_classes = [IsOwnerOnly | permissions.IsAdminUser, permissions.IsAuthenticated]
#
#		if self.action == 'create':
#			permission_classes = [~permissions.IsAuthenticated]# | permissions.IsAuthenticated]
#
#		return [permission() for permission in permission_classes]

		

		

