from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
import rest_framework
from rest_framework.parsers import MultiPartParser, FormParser
import copy
import os
from django.conf import settings

from advert.serializers import AdvertSerializer, AdvertFileSerializer
from advert.serializers import ReplySerializer, ReplyFileSerializer
from advert.serializers import FullAdvertSerializer
from advert.models import Advert, Reply, AdvertFile, ReplyFile
from advert.permissions import IsOwnerOnly, IsOwnerOnlyForAdvertFile
from advert.permissions import IsOwnerOnly, IsOwnerOnlyForReplyFile
from advert.permissions import IsStaffOnly


class AdvertViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = AdvertSerializer

	def get_queryset(self):

		queryset = Advert.objects.all().order_by('-created')

		return queryset
	
	def get_permissions(self):

		read_only_set = {'status', 'created', 'updated'}
		permission_classes = [permissions.IsAuthenticated, ]

		if self.request.method  in ['PUT', 'PATCH', 'POST']:
			request_keys = set(self.request.data.keys())
			if len(read_only_set.intersection(request_keys)) != 0:
			    self.permission_classes = [permissions.IsAdminUser & (~permissions.IsAuthenticated), ]
			else:
				self.permission_classes = [IsOwnerOnly, ]

		return super(AdvertViewSet, self).get_permissions()

	def get_serializer_context(self):
		context = super(AdvertViewSet, self).get_serializer_context()
		context.update({"request": self.request})
		return context

	def retrieve(self, request, pk=None):

		self.serializer_class = FullAdvertSerializer

		return super(AdvertViewSet, self).retrieve(self)


class ReplyViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = ReplySerializer

	def get_queryset(self):

		queryset = Reply.objects.all().order_by('-created')

		return queryset
	
	def get_permissions(self):

		read_only_set = {'author', 'created', 'updated'}
		permission_classes = [permissions.IsAuthenticated, ]

		if self.request.method  in ['PUT', 'PATCH', 'POST']:
			request_keys = set(self.request.data.keys())
			if len(read_only_set.intersection(request_keys)) != 0:
			    self.permission_classes = [permissions.IsAdminUser & (~permissions.IsAuthenticated), ]
			else:
				self.permission_classes = [IsOwnerOnly, ]

		return super(ReplyViewSet, self).get_permissions()

	def get_serializer_context(self):
		context = super(ReplyViewSet, self).get_serializer_context()
		context.update({"request": self.request})
		return context


class AdvertFileViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = AdvertFileSerializer
	parser_classes = (MultiPartParser, FormParser,)

	def get_queryset(self):

		queryset = AdvertFile.objects.all().order_by('-id')
		
		return queryset
	
	def get_serializer_context(self):
		context = super(AdvertFileViewSet, self).get_serializer_context()
		context.update({"request": self.request})
		return context

	def destroy(self, request, pk=None):

		advert_f = AdvertFile.objects.get(id=pk)
		full_file_name = settings.MEDIA_ROOT + '/' + advert_f.advert_file.name
		try:
			os.remove(full_file_name)
		except Exception as e:
			print('File error:', e)
		return super(AdvertFileViewSet, self).destroy(self)

	def get_permissions(self):

		self.permission_classes = (IsOwnerOnlyForAdvertFile | (IsStaffOnly&permissions.IsAuthenticated), )

		if self.request.method  in ['PUT', 'PATCH', ]:
			self.permission_classes = [permissions.IsAdminUser & (~permissions.IsAuthenticated), ]

		return super(AdvertFileViewSet, self).get_permissions()


class ReplyFileViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be created, viewed, edited or deleted.
	"""	
	serializer_class = ReplyFileSerializer
	parser_classes = (MultiPartParser, FormParser,)

	def get_queryset(self):

		queryset = ReplyFile.objects.all().order_by('-id')
		
		return queryset
	
	def get_serializer_context(self):
		context = super(ReplyFileViewSet, self).get_serializer_context()
		context.update({"request": self.request})
		return context

	def destroy(self, request, pk=None):

		reply_f = ReplyFile.objects.get(id=pk)
		full_file_name = settings.MEDIA_ROOT + '/' + reply_f.reply_file.name
		try:
			os.remove(full_file_name)
		except Exception as e:
			print('File error:', e)
		return super(ReplyFileViewSet, self).destroy(self)

	def get_permissions(self):

		self.permission_classes = (IsOwnerOnlyForReplyFile | (IsStaffOnly&permissions.IsAuthenticated), )

		if self.request.method  in ['PUT', 'PATCH', ]:
			self.permission_classes = [permissions.IsAdminUser & (~permissions.IsAuthenticated), ]

		return super(ReplyFileViewSet, self).get_permissions()
