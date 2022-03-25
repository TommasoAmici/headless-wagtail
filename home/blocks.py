from wagtail.core.blocks import RichTextBlock
from wagtail.core.rich_text import expand_db_html
from wagtail.images.blocks import ImageChooserBlock

from .fields import ImageRenditionField


class CustomRichTextBlock(RichTextBlock):
    def get_api_representation(self, value, context=None):
        return expand_db_html(value.source)


class CustomImageChooserBlock(ImageChooserBlock):
    def get_api_representation(self, value, context=None):
        return ImageRenditionField(
            ["width-512", "width-1024", "width-1536"]
        ).to_representation(value)
