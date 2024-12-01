from rest_framework import serializers
from .models import VikingsShow, NorsemenShow, VikingsNFL, CareerStat


class VikingsShowSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        """"""

        model = VikingsShow
        fields = "__all__"


class NorsemenShowSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        """"""

        model = NorsemenShow
        fields = "__all__"


class CareerStatSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = CareerStat
        fields = "__all__"


class VikingsNFLSerializer(serializers.ModelSerializer):
    """"""

    career_stats = CareerStatSerializer(many=True, read_only=True)

    class Meta:
        """"""

        model = VikingsNFL
        fields = "__all__"
