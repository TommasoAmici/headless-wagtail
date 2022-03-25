import urllib.parse

from django import forms
from django.conf import settings
from django.db import models
from django.http.response import HttpResponseRedirect, JsonResponse
from django.utils.module_loading import import_string
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from .blocks import CustomImageChooserBlock, CustomRichTextBlock


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
                urllib.parse.urljoin(settings.BASE_URL, full_path)
            )


class HomePage(BasePage):
    serializer_class = "home.serializers.HomePageSerializer"
    body = StreamField(
        [
            ("paragraph", CustomRichTextBlock()),
        ],
    )

    content_panels = [
        FieldPanel("title"),
        StreamFieldPanel("body"),
    ]


class ArticlePage(BasePage):
    serializer_class = "home.serializers.ArticlePageSerializer"
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    body = StreamField(
        [
            ("paragraph", CustomRichTextBlock()),
            ("image", CustomImageChooserBlock(icon="image")),
            ("table", TableBlock()),
        ],
    )

    content_panels = [
        FieldPanel("title"),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("body"),
    ]
