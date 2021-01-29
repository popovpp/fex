from rest_framework import serializers

from advert.models import Advert, Reply, AdvertFile, ReplyFile
from account.models import User
#from account.serializers import UserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
    	model = User
    	fields = ['email']


class AdvertSerializer(serializers.ModelSerializer):
	
#	id = serializers.IntegerField(read_only=False)
	author = User(UserSerializer()).email
	status = serializers.CharField(read_only=True)
	created = serializers.DateTimeField(read_only=True)
	updated = serializers.DateTimeField(read_only=True)

	class Meta:
		model = Advert
		fields = ['url', 'id', 'type_of_advert', 'title', 'description', 
		          'author', 'status', 'price', 'deadline', 'created',
		          'updated', 'active_until_date']


class ReplySerializer(serializers.ModelSerializer):

	class AdvertSerializer(serializers.ModelSerializer):
		class Meta:
			model = Advert
			fields = ['id']

	advert_id = Advert(AdvertSerializer()).id
	author = User(UserSerializer()).email
	created = serializers.DateTimeField(read_only=True)
	updated = serializers.DateTimeField(read_only=True)

	class Meta:
		model = Reply
		fields = ['url', 'id', 'advert_id', 'message', 'author', 'planed_date',
				  'price', 'created', 'updated']


class AdvertFileSerializer(serializers.ModelSerializer):

    advert_id = AdvertSerializer(read_only=True)
    advert_file = serializers.FileField(read_only=True)

    class Meta:
    	model = AdvertFile
    	fields = ['url', 'id', 'advert_id', 'advert_file']


class ReplyFileSerializer(serializers.ModelSerializer):
	
	reply_id = ReplySerializer(read_only=True)
	reply_file = serializers.FileField(read_only=True)

	class Meta:
		model = ReplyFile
		fields = ['url', 'id', 'reply_id', 'reply_file']
