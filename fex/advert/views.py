from django.shortcuts import render
# from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions

from advert.serializers import AdvertSerializer, AdvertFileSerializer
from advert.serializers import ReplySerializer, ReplyFileSerializer
from advert.models import Advert, Reply, AdvertFile, ReplyFile
from advert.permissions import IsOwnerOnly


class AdvertViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = AdvertSerializer

	def get_queryset(self):

		queryset = Advert.objects.all().order_by('-created')

		return queryset
	
	def get_permissions(self):

		read_only_set = {'author', 'status', 'created', 'updated'}
		permission_classes = [permissions.IsAuthenticated, ]

		if self.request.method  in ['PUT', 'PATCH', 'POST']:
			request_keys = set(self.request.data.keys())
			if len(read_only_set.intersection(request_keys)) != 0:
			    self.permission_classes = [permissions.IsAdminUser & (~permissions.IsAuthenticated), ]
			else:
				self.permission_classes = [IsOwnerOnly, ]

		return super(AdvertViewSet, self).get_permissions()


class ReplyViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = ReplySerializer

	def get_queryset(self):

		queryset = Reply.objects.all().order_by('-created')

		return queryset
	
	def get_permissions(self):

		read_only_set = {'author', 'advert_id', 'created', 'updated'}
		permission_classes = [permissions.IsAuthenticated, ]

		if self.request.method  in ['PUT', 'PATCH', 'POST']:
			request_keys = set(self.request.data.keys())
			if len(read_only_set.intersection(request_keys)) != 0:
			    self.permission_classes = [permissions.IsAdminUser & (~permissions.IsAuthenticated), ]
			else:
				self.permission_classes = [IsOwnerOnly, ]

		return super(ReplyViewSet, self).get_permissions()

	def create(self, request, *args, **kwargs):
		self.request.data['author'] = self.request.user
		print('ZZZZZZZZZZZZZZZZ')
		return super().create(self, self.request, *args, **kwargs)