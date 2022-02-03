from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import SingleTableView
from .models import Post
from .tables import PostTable
from .forms import PostForm


# Create your views here.


class PostListView(SingleTableView):
    model = Post
    table_class = PostTable
    # template_name = "blog/post_list.html"


class PostDetailView(DetailView):
    model = Post
    # template_name = "blog/post_details.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "text"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "text"]

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy("post_detail", kwargs={"pk": pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")
