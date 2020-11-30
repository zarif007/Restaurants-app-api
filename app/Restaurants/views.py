from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Item

from Restaurants import serializers


class BaseRestAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base viewset for user owned restaurants attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authentication user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        """Create a new objects"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRestAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.object.all()
    serializer_class = serializers.TagSerializer


class itemViewSet(BaseRestAttrViewSet):
    """Manage items in the database"""
    queryset = Item.object.all()
    serializer_class = serializers.ItemSerializer

