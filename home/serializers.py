from rest_framework import serializers
from wagtail.api.v2 import serializers as wagtail_serializers
from wagtail.core import fields

from .fields import ImageRenditionField
from .models import ArticlePage, BasePage, HomePage


class BasePageSerializer(serializers.ModelSerializer):
    serializer_field_mapping = (
        serializers.ModelSerializer.serializer_field_mapping.copy()
    )
    serializer_field_mapping.update(
        {fields.StreamField: wagtail_serializers.StreamField}
    )

    class Meta:
        model = BasePage
        fields = (
            "id",
            "slug",
            "title",
            "url",
            "first_published_at",
        )


class HomePageSerializer(BasePageSerializer):
    class Meta:
        model = HomePage
        fields = BasePageSerializer.Meta.fields + ("body",)


class ArticlePageSerializer(BasePageSerializer):
    feed_image = ImageRenditionField()

    class Meta:
        model = ArticlePage
        fields = BasePageSerializer.Meta.fields + ("body", "feed_image")
