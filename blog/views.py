from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Post
from .tables import PostTable

from .permissions import OwnershipRequiredMixin


# Create your views here.


class PostListView(ExportMixin, SingleTableView):
    model = Post
    template_name = "blog/post_list.html"
    table_class = PostTable
    table_pagination = {"per_page": 15}
    export_formats = ["csv", "json", "xls"]

    def get_queryset(self):
        posts = Post.objects.order_by("id")
        return posts


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("post_detail", kwargs={"pk": pk})


class PostUpdateView(LoginRequiredMixin, OwnershipRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "text"]

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("post_detail", kwargs={"pk": pk})


class PostDeleteView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
