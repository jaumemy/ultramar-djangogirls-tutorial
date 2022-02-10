import django_tables2 as tables
from .models import Post


class PostTable(tables.Table):
    detail = tables.TemplateColumn(
        """<a href="{{ record.get_absolute_url }}">See Detail</a>""",
        orderable=False,
    )
    created_date = tables.DateTimeColumn()
    options = tables.TemplateColumn(
        """
            {% if user.is_authenticated %}
            <a class="btn btn-default" href="{% url 'post_update' record.id %}"><span class="glyphicon glyphicon-pencil"></span></a>
            <a class="btn btn-default" href="{% url 'post_delete' record.id %}"><span class="glyphicon glyphicon-trash"></span></a>
            {% endif %}
        </a>
        """,
        orderable=False,
    )

    class Meta:
        model = Post
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "id",
            "author",
            "title",
            "text",
            "created_date",
            "last_updated_date",
            "options",
            "detail",
        )


class AuthorPostTable(PostTable):
    class Meta(PostTable.Meta):
        fields = (
            "id",
            "title",
            "text",
            "created_date",
            "last_updated_date",
            "options",
            "detail",
        )
