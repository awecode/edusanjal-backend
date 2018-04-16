from rest_framework import serializers

from .models import Board, Program


class BoardMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'slug', 'name')


class ProgramMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('id', 'name', 'slug', 'level')
