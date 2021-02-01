from rest_framework import serializers
import django.utils.timezone

from advert.models import Advert, Reply, AdvertFile, ReplyFile
from account.models import User
#from account.serializers import UserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
    	model = User
    	fields = ['email']


class AdvertSerializer(serializers.ModelSerializer):
	
	author = UserSerializer(read_only=True)
	status = serializers.CharField(read_only=True)
	created = serializers.DateTimeField(read_only=True)
	updated = serializers.DateTimeField(read_only=True)
	active_until_date = serializers.DateTimeField(default=django.utils.timezone.now)

	class Meta:
		model = Advert
		fields = ['url', 'id', 'type_of_advert', 'title', 'description', 
		          'author', 'status', 'price', 'deadline', 'created',
		          'updated', 'active_until_date']
    
	def create(self, *args, **kwargs):
		advert = Advert.objects.create(author=self.context['request'].user)
		advert.type_of_advert = self.validated_data.get('type_of_advert', 
			                                            self.context['request'].data['type_of_advert'])
		advert.title = self.validated_data.get('title', 
			                                   self.context['request'].data['title'])
		advert.description = self.validated_data.get('description', 
			                                         self.context['request'].data['description'])
		advert.price = self.validated_data.get('price', 
			                                    self.context['request'].data['price'])
		advert.deadline = self.validated_data.get('deadline', 
			                                       self.context['request'].data['deadline'])
		advert.active_until_date = self.validated_data.get('active_until_date', 
			                                                self.context['request'].data['active_until_date'])
		advert.save()
		return advert


class ReplySerializer(serializers.ModelSerializer):

	class AdvertSerializer(serializers.ModelSerializer):
		class Meta:
			model = Advert
			fields = ['id']

	advert_id = AdvertSerializer(read_only=True)
	author = UserSerializer(read_only=True)
	created = serializers.DateTimeField(read_only=True)
	updated = serializers.DateTimeField(read_only=True)
	price = serializers.IntegerField(default=0)

	class Meta:
		model = Reply
		fields = ['url', 'id', 'advert_id', 'message', 'author', 'planed_date',
				  'price', 'created', 'updated']

	def create(self, *args, **kwargs):
		reply = Reply.objects.create(author=self.context['request'].user, 
			                         advert_id=Advert.objects.get(id=self.context['request'].
			                         data['advert_id']['id']))
		reply.message = self.validated_data.get('message', 
			                                    self.context['request'].data['message'])
		reply.planed_date = self.validated_data.get('planed_date', 
			                                        self.context['request'].data['planed_date'])
		reply.price = self.validated_data.get('price', 
			                                  self.context['request'].data['price'])
		reply.save()
		return reply

	def update(self, pk, *args, **kwargs):
		reply = Reply.objects.get(id=pk.id)
		reply.message = self.validated_data.get('message', 
			                                    self.context['request'].data['message'])
		reply.planed_date = self.validated_data.get('planed_date', 
			                                        self.context['request'].data['planed_date'])
		reply.price = self.validated_data.get('price', 
			                                  self.context['request'].data['price'])
		reply.save()
		return reply


class AdvertFileSerializer(serializers.ModelSerializer):

    class AdvertSerializer(serializers.ModelSerializer):
    	class Meta:
    		model = Advert
    		fields = ['id']

#    advert_id = AdvertSerializer(read_only=True)
    advert_file = serializers.FileField(read_only=True)

    class Meta:
    	model = AdvertFile
#    	fields = ['url', 'id', 'advert_id', 'advert_file']
    	fields = ['url', 'id', 'advert_file']

#    def create(self, *args, **kwargs):
#    	advert_f = AdvertFile.objects.create(advert_id=Advert.objects.get(id=self.context['request'].
#			                                 data['advert_id']['id']))
#    	advert_f.advert_file = self.validated_data.get('advert_file', 
#    		                                           self.context['request'].data['advert_file'])
#    	print(self.context['request'].data['advert_file'])
#    	advert_f.save()
#    	return advert_f


class ReplyFileSerializer(serializers.ModelSerializer):
	
	reply_id = ReplySerializer(read_only=True)
	reply_file = serializers.FileField(read_only=True)

	class Meta:
		model = ReplyFile
		fields = ['url', 'id', 'reply_id', 'reply_file']
