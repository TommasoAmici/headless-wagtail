from collections import OrderedDict

from rest_framework.fields import Field
from wagtail.core.rich_text import expand_db_html
from wagtail.images.models import SourceImageIOError


class CustomRichTextField(Field):
    def to_representation(self, value):
        return expand_db_html(value).replace("/api", "")


class ImageRenditionField(Field):
    def __init__(
        self,
        filter_spec=["width-64", "width-128", "width-256", "width-512"],
        fallback="width-256",
        *args,
        **kwargs,
    ):
        self.filter_spec = filter_spec
        self.fallback = fallback
        super().__init__(*args, **kwargs)

    def to_representation(self, image):
        src = image.get_rendition(self.fallback)
        alt = src.alt
        srcset = ""
        srcset_webp = ""
        for filter_spec in self.filter_spec:
            thumbnail = image.get_rendition(filter_spec)
            thumbnail_webp = image.get_rendition(f"{filter_spec}|format-webp")
            srcset += f"{thumbnail.url} {thumbnail.width}w,"
            srcset_webp += f"{thumbnail_webp.url} {thumbnail_webp.width}w,"
        return {
            "alt": alt,
            "src": src.url,
            "srcset": srcset,
            "srcset_webp": srcset_webp,
        }
