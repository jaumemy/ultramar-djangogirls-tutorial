import django_tables2 as tables
from django_tables2.utils import A
from .models import Post


class PostTable(tables.Table):
    detail = tables.LinkColumn("post_detail", args=[A("pk")])

    class Meta:
        model = Post
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "id",
            "author",
            "title",
            "text",
            "created_date",
            "published_date",
        )
