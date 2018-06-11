from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from .documents import ProgramDoc
from .models import Board, Program


class BoardMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('slug', 'name')


class ProgramMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('name', 'slug', 'level')


class ProgramDocSerializer(DocumentSerializer):
    class Meta:
        document = ProgramDoc
        fields = ('slug', 'name', 'full_name', 'short_name', 'discipline')
