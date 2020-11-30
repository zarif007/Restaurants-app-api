from rest_framework import serializers

from core.models import Tag, Item


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ItemSerializer(serializers.ModelSerializer):
    """Serailizers for item objects"""

    class Meta:
        model = Item
        fields = ('id', 'name')
        read_only_fields = ('id',)
