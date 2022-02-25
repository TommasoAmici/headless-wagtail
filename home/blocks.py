from wagtail.core.blocks import RichTextBlock
from wagtail.core.rich_text import expand_db_html


class CustomRichTextBlock(RichTextBlock):
    def get_api_representation(self, value, context=None):
        return expand_db_html(value.source).replace("/api", "")
