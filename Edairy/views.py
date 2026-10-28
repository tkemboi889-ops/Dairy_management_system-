from django.shortcuts import render




from django.urls import reverse_lazy

from .models import Calf, Cow, Worker, Feed, farm_manager, Milk
from .forms import (
    calform,
    cowform,
    milkform,
    feedform,
    workerform,
    farmerform,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
CreateView,
ListView,
UpdateView,
DetailView,
DeleteView,
)

from .models import Calf, Cow, Worker, Feed, farm_manager, Milk
from .forms import (
calform,
cowform,
feedform,
workerform,
farmerform,
milkform,
)

def dashboard(reguest):
    return render(reguest,"Edairy:base.html")

# CALF VIEWS



class add_calf(PermissionRequiredMixin, CreateView):
 model = Calf
 form_class = calform
 template_name = "edairy/calf/calf_form.html"
 success_url = reverse_lazy("Edairy:calfs_list")
 permission_required = "edairy.add_calf"

class calfs_list(ListView):
 model = Calf
 template_name = "edairy/calf/calf_list.html"

class update_calfs(PermissionRequiredMixin, UpdateView):
 model = Calf
 form_class = calform
 template_name = "edairy/calf/calf_update.html"
 success_url = reverse_lazy("Edairy:calfs_list")
 permission_required = "edairy.change_calf"

class calf_details(DetailView):
 model = Calf
 template_name = "edairy/calf/calf_detail.html"

class delete_calf(PermissionRequiredMixin, DeleteView):
 model = Calf
 template_name = "edairy/calf/calf_confirm_delete.html"
 permission_required = "edairy.delete_calf"
 success_url = reverse_lazy("Edairy:calfs_list")



# COW VIEWs

class add_cow(PermissionRequiredMixin, CreateView):
 model = Cow
 form_class = cowform
 template_name = "edairy/cow/cow_form.html"
 success_url = reverse_lazy("Edairy:cow_list")
 permission_required = "edairy.add_cow"

class cows_list(ListView):
 model = Cow
 template_name = "edairy/cow/cow_list.html"

class update_cows(PermissionRequiredMixin, UpdateView):
 model = Cow
 form_class = cowform
 template_name = "edairy/cow/cow_update.html"
 success_url = reverse_lazy("Edairy:cow_list")
 permission_required = "edairy.change_cow"

class cow_details(DetailView):
 model = Cow
 template_name = "edairy/cow/cow_detail.html"

class delete_cow(PermissionRequiredMixin, DeleteView):
 model = Cow
 template_name = "edairy/cow/cow_confirm_delete.html"
 permission_required = "edairy.delete_cow"
 success_url = reverse_lazy("Edairy:cow_list")



# FEED VIEWS



class add_feeds(PermissionRequiredMixin, CreateView):
 model = Feed
 form_class = feedform
 template_name = "edairy/feed/feed_form.html"
 success_url = reverse_lazy("Edairy:feeds_list")
 permission_required = "edairy.add_feed"

class feeds_list(ListView):
 model = Feed
 template_name = "edairy/feed/feed_list.html"

class feeds_update(PermissionRequiredMixin, UpdateView):
 model = Feed
 form_class = feedform
 template_name = "edairy/feed/feed_update.html"
 success_url = reverse_lazy("Edairy:feeds_list")
 permission_required = "edairy.change_feed"

class feed_details(DetailView):
 model = Feed
 template_name = "edairy/feed/feed_detail.html"

class delete_feeds(PermissionRequiredMixin, DeleteView):
 model = Feed
 template_name = "edairy/feed/feed_confirm_delete.html"
 permission_required = "edairy.delete_feed"
 success_url = reverse_lazy("Edairy:feeds_list")

#  worker model

class add_workers(PermissionRequiredMixin, CreateView):
  model = Worker
  form_class = workerform
  template_name = "edairy/worker/worker_form.html"
  success_url = reverse_lazy("Edairy:workers_list")
  permission_required = "edairy.add_worker"

class workers_list(ListView):
 model = Worker
 template_name = "edairy/worker/worker_list.html"

class update_workers(PermissionRequiredMixin, UpdateView):
 model = Worker
 form_class = workerform
 template_name = "edairy/worker/worker_update.html"
 success_url = reverse_lazy("Edairy:workers_list")
 permission_required = "edairy.change_worker"

class worker_details(DetailView):
 model = Worker
 template_name = "edairy/worker/worker_detail.html"

class delete_worker(PermissionRequiredMixin, DeleteView):
 model = Worker
 template_name = "edairy/worker/worker_confirm_delete.html"
 permission_required = "edairy.delete_worker"
 success_url = reverse_lazy("Edairy:workers_list")



# FARM MANAGER VIEWS


class add_farmer(PermissionRequiredMixin, CreateView):
 model = farm_manager
 form_class = farmerform
 template_name = "edairy/farmer/farmer_form.html"
 success_url = reverse_lazy("Edairy:farmers_list")
 permission_required = "edairy.add_farmer"

class farmers_list(ListView):
 model = farm_manager
 template_name = "edairy/farmer/farmer_list.html"

class farmers_update(PermissionRequiredMixin, UpdateView):
 model = farm_manager
 form_class = farmerform
 template_name = "edairy/farmer/farmer_update.html"
 success_url = reverse_lazy("Edairy:farmers_list")
 permission_required = "edairy.change_farmer"

class farmers_detail(DetailView):
 model = farm_manager
template_name = "edairy/farmer/farmer_detail.html"

class delete_farmer(PermissionRequiredMixin, DeleteView):
 model = farm_manager
 template_name = "edairy/farmer/farmer_confirm_delete.html"
 permission_required = "edairy.delete_farmer"
 success_url = reverse_lazy("Edairy:farmers_list")


# MILK VIEWS

class add_milk(PermissionRequiredMixin, CreateView):
 model = Milk
 form_class = milkform
 template_name = "edairy/milk/milk_form.html"
 success_url = reverse_lazy("Edairy:milk_list")
 permission_required = "edairy.add_milk"

class milk_list(ListView):
 model = Milk
 template_name = "edairy/milk/milk_list.html"

class update_milk(PermissionRequiredMixin, UpdateView):
 model = Milk
 form_class = milkform
 template_name = "edairy/milk/milk_update.html"
 success_url = reverse_lazy("Edairy:milk_list")
 permission_required = "edairy.change_milk"

class milk_details(DetailView):
 model = Milk
 template_name = "edairy/milk/milk_detail.html"

class delete_milk(PermissionRequiredMixin, DeleteView):
 model = Milk
 template_name = "edairy/milk/milk_confirm_delete.html"
 permission_required = "edairy.delete_milk"
 success_url = reverse_lazy("Edairy:milk_list")
