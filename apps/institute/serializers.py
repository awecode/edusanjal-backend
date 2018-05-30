from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers
from versatileimagefield.utils import build_versatileimagefield_url_set

from apps.institute.documents import InstituteDoc
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
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return build_versatileimagefield_url_set(obj.file, obj.sizes, self.context.get('request'))

    class Meta:
        model = InstituteImage
        fields = ('name', 'url')


class InstituteMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ('name', 'logo_set', 'slug', 'levels')


class InstituteDetailSerializer(serializers.ModelSerializer):
    boards = BoardMinSerializer(many=True)
    recent_awards = AwardMinSerializer(many=True)
    documents = InstituteDocumentSerializer(many=True)
    images = InstituteImageSerializer(many=True)
    network_institutes = serializers.SerializerMethodField()
    programs = ProgramMinSerializer(many=True)

    # logo = serializers.ReadOnlyField(source='logo_set')

    def get_network_institutes(self, obj):
        return InstituteMinSerializer(obj.network_institutes.prefetch_related('programs'), many=True, context=self.context).data

    class Meta:
        model = Institute
        fields = (
            'name', 'slug', 'cover_image', 'logo_set', 'boards', 'verified', 'description', 'recent_awards', 'awards_count',
            'documents', 'established', 'address', 'district', 'type', 'phone', 'email', 'website', 'images', 'salient_features',
            'admission_guidelines', 'scholarship_information', 'network_institutes', 'levels', 'programs', 'institute_personnels',
            'latitude', 'longitude')


class InstituteDocSerializer(DocumentSerializer):
    class Meta:
        document = InstituteDoc
        fields = ('name', 'logo_set', 'slug', 'address', 'verified', 'is_member', 'featured', 'type', 'boards')
