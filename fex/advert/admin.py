from django.contrib import admin
from advert.models import Advert
from advert.models import AdvertFile
from advert.models import Reply
from advert.models import ReplyFile


class AdvertModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'type_of_advert', 'title', 'description', 'author',
	                'status', 'price', 'deadline', 'created', 'updated',
	                'active_until_date']
	list_display_links = ['id']
	list_filter = ['created', 'updated']
	search_fields = ['id', 'title']
	# list_editable = ['title', 'description']
	# inlines = [PostInstanceInline]
	# fields = ('title',)
	# exclude = ('post_likes',)


	class Meta:
		model = Advert


class ReplyModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'advert_id', 'message', 'author', 'planed_date',
	                'price', 'created', 'updated']
	list_display_links = ['id']
	list_filter = ['advert_id', 'author']
	search_fields = ['advert_id', 'author']

	class Meta:
		model = Reply


class ReplyFileModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'reply_id', 'reply_file']
	list_display_links = ['id']
	list_filter = ['reply_id']
	search_fields = ['reply_id']

	class Meta:
		model = ReplyFile


class AdvertFileModelAdmin(admin.ModelAdmin):
	list_display = ['id', 'advert_id', 'advert_file']
	list_display_links = ['id']
	list_filter = ['advert_id']
	search_fields = ['advert_id']

	class Meta:
		model = AdvertFile


admin.site.register(Advert, AdvertModelAdmin)
admin.site.register(Reply, ReplyModelAdmin)
admin.site.register(ReplyFile, ReplyFileModelAdmin)
admin.site.register(AdvertFile, AdvertFileModelAdmin)
