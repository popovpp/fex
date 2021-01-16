from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework import permissions
from account.serializers import UserSerializer, UserSerializer_1
from account.models import User
from account.permissions import IsOwnerOnly
#from django.http import Http404
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""	

	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer
	permission_classes = [IsOwnerOnly]


#class UserList(APIView):
#    """
#    
#    """
#    def get(self, request, format=None):
#        users = User.objects.all()
#        serializer = UserSerializer(many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = UserSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#class UserDetail(APIView):
#    """
#    Retrieve, update or delete a snippet instance.
#    """
#    def get_object(self, pk):
#        try:
#            return User.objects.get(pk=pk)
#        except User.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        user = self.get_object(pk)
#        serializer = UserSerializer()
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        user = self.get_object(pk)
#        serializer = UserSerializer( data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        user = self.get_object(pk)
#        user.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
