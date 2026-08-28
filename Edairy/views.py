from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
)

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
from django.contrib.auth.mixins import PermissionRequiredMixin
# a view to handle calf model
class AddCalfView(PermissionRequiredMixin, CreateView):
    model = Calf
    form_class = calform
    template_name = "edairy/calf/calf_form.html"
    success_url = reverse_lazy("calfs_list")


class calfs_list(ListView):
    model=Calf
    template_name="edairy/calf/calf_list.html"

class update_calfs(UpdateView):
    model=Calf
    form_class=calform
    template_name="edairy/calf/calf_update.html"
    success_url=reverse_lazy("calfs_list")

class calf_details(DetailView):
    model=Calf
    template_name="edairy/calf/calf_detail.html"
    success_url=reverse_lazy("calfs_list")

class delete_calf(DeleteView):
    model=Calf
    template_name="edairy/calf/calf_confirm_delate.html"

    # View to handle cow model
class add_cow( PermissionRequiredMixin,CreateView):
    model=Cow
    form_class=cowform
    template_name="edairy/cow/cow_form.html"
    success_url=reverse_lazy("cows_list")

class cows_list(ListView):
    model=Cow
    template_name="edairy/cow/cow_list.html"

class update_cows(PermissionRequiredMixin,UpdateView):
    model=Cow
    form_class=cowform
    template_name="edairy/cow/cow_update.html"
    success_url=reverse_lazy("cows_list")

class cow_details(DetailView):
    model=Cow
    template_name="edairy/cow/cow_detail.html"
    success_url=reverse_lazy("cows_list")

class delete_cow(DeleteView):
    model=Cow
    template_name="edairy/cow/cow_confirm_delete.html"

    # view to handle feeds
class add_feeds(PermissionRequiredMixin,CreateView):
    model=Feed
    form_class=feedform
    template_name="edairy/feed/feed_form.html"
    success_url=reverse_lazy("feeds_list")

class feeds_list(ListView):
    model=Feed
    template_name="edairy/feed/feed_list.html"

class feeds_update(PermissionRequiredMixin,UpdateView):
    model=Feed
    form_class=feedform
    template_name="edairy/feed/feed_update.html"
    success_url=reverse_lazy("feeds_list")

class feed_details(DetailView):
    model=Feed
    template_name="edairy/feed/feed_detail.html"
    success_url=reverse_lazy("feeds_list")

class delete_feeds(DeleteView):
    model=Feed
    template_name="edairy/feed/feed_confirm_delete.html"

# view to handle worker model
class add_workers(PermissionRequiredMixin,CreateView):
    model=Worker
    form_class=workerform
    template_name="edairy/worker/worker_form.html"
    success_url=reverse_lazy("workers_list")

class workers_list(ListView):
    model=Worker
    template_name="edairy/worker/worker_list.html"

class update_workers(PermissionRequiredMixin,UpdateView):
    model=Worker
    form_class=workerform
    template_name="edairy/worker/worker_update.html"
    success_url=reverse_lazy("workers_list")

class worker_details(DetailView):
    model=Worker
    template_name="edairy/worker/worker_detail.html"
    success_url=reverse_lazy("workers_list")

class delete_worker(DeleteView):
    model=Worker
    template_name="edairy/worker/worker_confirm_delete.html"

# view to handle farmer model
class add_farmer(PermissionRequiredMixin,CreateView):
    model=farm_manager
    form_class=farmerform
    template_name="edairy/farmer/farmer_form.html"
    success_url=reverse_lazy("farmers_list")

class farmers_list(ListView):
    model=farm_manager
    template_name="edairy/farmer/farmer_list.html"

class farmers_update(PermissionRequiredMixin,UpdateView):
    model=farm_manager
    form_class=farmerform
    template_name="edairy/farmer/farmer_update.html"
    success_url=reverse_lazy("farmers_list")


class farmers_detail(DetailView):
    model=farm_manager
    template_name="edairy/farmer/farmer_detail.html"
    success_url=reverse_lazy("farmers_list")

class delete_farmer(DeleteView):
    model=farm_manager
    template_name="edairy/farmer/farmer_confirm_delete.html"

# view to handle milk model
class add_milk(PermissionRequiredMixin,CreateView):
    model=Milk
    form_class=milkform
    template_name="edairy/milk/milk_form.html"
    success_url=reverse_lazy("milk_list")

class milk_list(ListView):
    model=Milk
    template_name="edairy/milk/milk_list.html"

class update_milk(PermissionRequiredMixin,UpdateView):
    model=Milk
    form_class=milkform
    template_name="edairy/milk/milk_update.html"
    success_url=reverse_lazy("milk_list")

class milk_details(DetailView):
    model=Milk
    template_name="edairy/milk/milk_detail.html"
    success_url=reverse_lazy("milk_list")

class delete_milk(DeleteView):
    model=Milk
    template_name="edairy/milk/milk_confirm_delete.html"

