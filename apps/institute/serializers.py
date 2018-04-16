from rest_framework import serializers

from ..program.serializers import BoardMinSerializer, ProgramMinSerializer
from .models import Institute, Award, InstituteDocument, InstituteImage


class AwardMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ('slug', 'name')


class InstituteDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteDocument
        fields = ('name', 'file')


class InstituteImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteImage
        fields = ('name', 'file')


class InstituteMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ('name', 'logo', 'slug', 'levels')


class InstituteDetailSerializer(serializers.ModelSerializer):
    boards = BoardMinSerializer(many=True)
    recent_awards = AwardMinSerializer(many=True)
    documents = InstituteDocumentSerializer(many=True)
    images = InstituteDocumentSerializer(many=True)
    network_institutes = serializers.SerializerMethodField()
    programs = ProgramMinSerializer(many=True)
    
    def get_network_institutes(self, obj):
        return InstituteMinSerializer(obj.network_institutes.prefetch_related('programs'), many=True).data
    

    class Meta:
        model = Institute
        fields = (
            'name', 'cover_image', 'logo', 'boards', 'description', 'recent_awards', 'awards_count', 'documents', 'established',
            'address', 'district', 'type', 'phone', 'email', 'website', 'images', 'salient_features', 'admission_guidelines',
            'scholarship_information', 'network_institutes', 'levels', 'programs')
