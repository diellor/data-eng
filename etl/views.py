from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import VikingsShow, NorsemenShow, VikingsNFL
from .serializers import (
    VikingsShowSerializer,
    NorsemenShowSerializer,
    VikingsNFLSerializer,
)


class BaseShowViewSet(viewsets.ModelViewSet):
    """A base View Set class for get requests."""

    http_method_names = ["get"]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["actor_name", "character_name"]

    search_fields = []
    filterset_fields = []


class VikingsShowViewSet(BaseShowViewSet):
    """Viewset for the VikingsShow model."""

    queryset = VikingsShow.objects.all()
    serializer_class = VikingsShowSerializer

    search_fields = [
        "actor_url",
        "img_src",
        "actor_name",
        "character_name",
        "character_description",
    ]
    filterset_fields = ["actor_url", "actor_name", "character_name"]


class NorsemenShowViewSet(BaseShowViewSet):
    """Viewset for the NorsemenShow model."""

    queryset = NorsemenShow.objects.all()
    serializer_class = NorsemenShowSerializer

    search_fields = ["actor_name", "character_name", "description"]
    filterset_fields = ["actor_name", "character_name"]


class NFLVikingsShowViewSet(BaseShowViewSet):
    """Viewset for the NorsemenShow model."""

    queryset = VikingsNFL.objects.all()
    serializer_class = VikingsNFLSerializer

    search_fields = ["player_name", "profile_link", "age"]
    filterset_fields = ["player_name", "profile_link"]
