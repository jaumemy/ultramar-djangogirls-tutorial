from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from .models import Post, PostUpdateEvent
from .tables import PostTable, AuthorPostTable

from .permissions import OwnershipRequiredMixin


# Create your views here.


class PostListView(ExportMixin, SingleTableView):
    model = Post
    table_class = PostTable
    table_pagination = {"per_page": 10}
    export_formats = ["csv", "json", "xls"]

    def get_queryset(self):
        posts = Post.objects.order_by("id")
        return posts


class AuthorPostListView(ExportMixin, SingleTableView):
    model = Post
    template_name = "blog/author_post_list.html"
    table_class = AuthorPostTable
    table_pagination = {"per_page": 10}
    export_formats = ["csv", "json", "xls"]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        posts = Post.objects.filter(author=pk).order_by("id")
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        author = User.objects.get(pk=pk)
        context["author"] = author
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        post_update_events = PostUpdateEvent.objects.filter(post=pk)
        context["post_update_events"] = post_update_events
        return context


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

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        pk = self.kwargs["pk"]

        date = timezone.now()
        post = Post.objects.get(pk=pk)
        post.last_updated_date = date
        post.save()
        PostUpdateEvent.objects.create(post=post, user=user, date=date)

        return super().form_valid(form)

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("post_detail", kwargs={"pk": pk})


class PostDeleteView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
