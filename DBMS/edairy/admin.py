from django.contrib import admin
from .models import Owner,Milk,Calf,Feed,Worker,Cow
# Register your models here.
admin.site.register(Owner)
admin.site.register(Milk)
admin.site.register(Calf)
admin.site.register(Feed)
admin.site.register(Worker)
admin.site.register(Cow)