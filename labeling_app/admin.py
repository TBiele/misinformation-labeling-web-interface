from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import TelegramMessage, Topic, Misconception, MessageMisconception

class TelegramMessageResource(resources.ModelResource):
   class Meta:
      model = TelegramMessage
class TelegramMessageAdmin(ImportExportModelAdmin):
   resource_class = TelegramMessageResource
admin.site.register(TelegramMessage, TelegramMessageAdmin)

class TopicResource(resources.ModelResource):
   class Meta:
      model = Topic
class TopicAdmin(ImportExportModelAdmin):
   resource_class = TopicResource
admin.site.register(Topic, TopicAdmin)

class MisconceptionResource(resources.ModelResource):
   class Meta:
      model = Misconception
class MisconceptionAdmin(ImportExportModelAdmin):
   resource_class = MisconceptionResource
admin.site.register(Misconception, MisconceptionAdmin)

class MessageMisconceptionResource(resources.ModelResource):
   class Meta:
      model = MessageMisconception
class MessageMisconceptionAdmin(ImportExportModelAdmin):
   resource_class = MessageMisconceptionResource
admin.site.register(MessageMisconception, MessageMisconceptionAdmin)