

# Register your models here.
from django.contrib import admin
from .models import farm_manager,Milk,Calf,Feed,Worker,Cow
# Register your models here.
admin.site.register(farm_manager)
admin.site.register(Milk)
admin.site.register(Calf)
admin.site.register(Feed)
admin.site.register(Worker)
admin.site.register(Cow)