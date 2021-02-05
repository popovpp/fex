from rest_framework import serializers
import django.utils.timezone
from os.path import basename

from advert.models import Advert, Reply, AdvertFile, ReplyFile
from account.models import User



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


class AdvertFileSerializer(serializers.ModelSerializer):

    class AdvertSerializer(serializers.ModelSerializer):
    	class Meta:
    		model = Advert
    		fields = ['id']

    advert_file = serializers.FileField(use_url=True)

    class Meta:
    	model = AdvertFile
    	fields = ['url', 'id', 'advert_id', 'advert_file']

    def create(self, *args, **kwargs):

        advert = Advert.objects.get(id=self.context['request'].data['advert_id'][0][0])
        advert_f = AdvertFile.objects.create(advert_file=self.context['request'].data['advert_file'], 
        	       advert_id=advert)#Advert.objects.get(id=self.context['request'].data['advert_id'][0][0]))
        
        advert_f.advert_file.name = basename(advert_f.advert_file.name)
        advert_f.save()
        
        advert.advert_file.add(advert_f)
        advert.save()
        return advert_f

    def update(self, pk, *args, **kwargs):

        advert_f = AdvertFile.objects.get(id=pk.id)     
        advert_f.advert_file = self.context['request'].data['advert_file']
        advert_f.advert_file = basename(advert_f.advert_file.name)
        advert_f.save()
        return advert_f


class ReplyFileSerializer(serializers.ModelSerializer):
	
	class ReplySerializer(serializers.ModelSerializer):
		class Meta:
			model = Reply
			fields = ['id']

	reply_file = serializers.FileField(use_url=True)

	class Meta:
		model = ReplyFile
		fields = ['url', 'id', 'reply_id', 'reply_file']

	def create(self, *args, **kwargs):

		reply = Reply.objects.get(id=self.context['request'].data['reply_id'])
		reply_f = ReplyFile.objects.create(reply_file=self.context['request'].data['reply_file'], 
        	                               reply_id=reply)
		reply_f.reply_file.name = basename(reply_f.reply_file.name)
		reply_f.save()
		reply.rep_file.add(reply_f)
		reply.save()
		return reply_f

	def update(self, pk, *args, **kwargs):

		reply_f = ReplyFile.objects.get(id=pk.id)     
		reply_f.reply_file = self.context['request'].data['reply_file']
		reply_f.reply_file = basename(reply_f.reply_file.name)
		reply_f.save()
		return reply_f


class ReplySerializer(serializers.ModelSerializer):

	class AdvertSerializer(serializers.ModelSerializer):
		class Meta:
			model = Advert
			fields = ['id']

	author = UserSerializer(read_only=True)
	created = serializers.DateTimeField(read_only=True)
	updated = serializers.DateTimeField(read_only=True)
	price = serializers.IntegerField(default=0)
	rep_file = ReplyFileSerializer(many=True, default='')


	class Meta:
		model = Reply
		fields = ['url', 'id', 'advert_id', 'message', 'author', 'planed_date',
				  'price', 'created', 'updated', 'rep_file']

	def create(self, *args, **kwargs):
		advert = Advert.objects.get(id=self.context['request'].
			                        data['advert_id'])
		reply = Reply.objects.create(author=self.context['request'].user, 
			                         advert_id=advert)
		reply.message = self.validated_data.get('message', 
			                                    self.context['request'].data['message'])
		reply.planed_date = self.validated_data.get('planed_date', 
			                                        self.context['request'].data['planed_date'])
		reply.price = self.validated_data.get('price', 
			                                  self.context['request'].data['price'])
		reply.save()
		advert.rep.add(reply)
		advert.save()
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


class FullAdvertSerializer(serializers.ModelSerializer):
	
	author = UserSerializer(read_only=True)
	status = serializers.CharField(read_only=True)
	created = serializers.DateTimeField(read_only=True)
	updated = serializers.DateTimeField(read_only=True)
	active_until_date = serializers.DateTimeField(default=django.utils.timezone.now)
	advert_file = AdvertFileSerializer(many=True)
	rep = ReplySerializer(many=True)

	class Meta:
		model = Advert
		fields = ['url', 'id', 'type_of_advert', 'title', 'description', 
		          'author', 'status', 'price', 'deadline', 'created',
		          'updated', 'active_until_date', 'advert_file', 'rep', ]
