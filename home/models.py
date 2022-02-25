import urllib.parse

from django import forms
from django.conf import settings
from django.db import models
from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils.module_loading import import_string
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock

from .blocks import CustomRichTextBlock


class BasePage(Page):
    serializer_class = None

    class Meta:
        abstract = True

    def serialize_page(self):
        """Serialize the Page using the serializer in `serializer_class`"""
        if not self.serializer_class:
            raise Exception(f"serializer_class is not set {self.__class__.__name__}")
        serializer_class = import_string(self.serializer_class)

        return {
            "type": self.__class__.__name__,
            "data": serializer_class(self).data,
        }

    def serve(self, request, *args, **kwargs):
        """
        If the request accepts JSON, returns an object with all the page's data.
        Otherwise it redirects to the rendered frontend.
        """
        if request.content_type == "application/json":
            reponse = self.serialize_page()
            return JsonResponse(reponse)
        else:
            full_path = request.get_full_path()
            return HttpResponseRedirect(
                urllib.parse.urljoin(settings.BASE_URL, full_path.replace("/api", ""))
            )


class ArticlePage(BasePage):
    serializer_class = "home.serializers.ArticlePageSerializer"

    summary = models.CharField(max_length=300)
    body = StreamField(
        [
            ("paragraph", CustomRichTextBlock()),
            ("image", ImageChooserBlock(icon="image")),
        ],
    )

    content_panels = [
        FieldPanel("title"),
        FieldPanel("summary", widget=forms.Textarea(attrs={"rows": "4"})),
        StreamFieldPanel("body"),
    ]
