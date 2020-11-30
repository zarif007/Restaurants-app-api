from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Item

from Restaurants import serializers


class TagViewSet(viewsets.GenericViewSet, 
                 mixins.ListModelMixin, 
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.object.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class itemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage items in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Item.object.all()
    serializer_class = serializers.ItemSerializer

    def get_queryset(self):
        """Returned objects for the current authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
