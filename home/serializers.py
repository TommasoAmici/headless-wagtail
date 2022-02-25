from rest_framework import serializers
from wagtail.api.v2 import serializers as wagtail_serializers
from wagtail.core import fields

from .models import ArticlePage, BasePage


class BasePageSerializer(serializers.ModelSerializer):
    serializer_field_mapping = serializers.ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping.update({fields.StreamField: wagtail_serializers.StreamField})

    class Meta:
        model = BasePage
        fields = (
            "id",
            "slug",
            "title",
            "url",
            "first_published_at",
        )


class ArticlePageSerializer(BasePageSerializer):
    class Meta:
        model = ArticlePage
        fields = BasePageSerializer.Meta.fields + (
            "summary",
            "body",
        )
