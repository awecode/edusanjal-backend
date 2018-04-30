from rest_framework import serializers
# from versatileimagefield.serializers import VersatileImageFieldSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer
from versatileimagefield.utils import build_versatileimagefield_url_set

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
    # file = VersatileImageFieldSerializer(sizes=[
    #     ('large', 'url'),
    #     ('thumbnail', 'thumbnail__100x100'),
    #     ('medium_square_crop', 'crop__400x400'),
    #     ('small_square_crop', 'crop__50x50')
    # ])
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        ret = build_versatileimagefield_url_set(obj.file, obj.sizes, self.context.get('request'))
        return ret

    #     return VersatileImageFieldSerializer(obj.file, [
    #     ('large', 'url'),
    #     ('medium', 'crop__400x400'),
    #     ('small', 'thumbnail__100x100')
    # ]).data

    class Meta:
        model = InstituteImage
        fields = ('name', 'url')


class InstituteMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ('name', 'logo', 'slug', 'levels')


class InstituteDetailSerializer(serializers.ModelSerializer):
    boards = BoardMinSerializer(many=True)
    recent_awards = AwardMinSerializer(many=True)
    documents = InstituteDocumentSerializer(many=True)
    images = InstituteImageSerializer(many=True)
    network_institutes = serializers.SerializerMethodField()
    programs = ProgramMinSerializer(many=True)

    def get_network_institutes(self, obj):
        return InstituteMinSerializer(obj.network_institutes.prefetch_related('programs'), many=True).data

    class Meta:
        model = Institute
        fields = (
            'name', 'slug', 'cover_image', 'logo', 'boards', 'verified', 'description', 'recent_awards', 'awards_count',
            'documents',
            'established', 'address', 'district', 'type', 'phone', 'email', 'website', 'images', 'salient_features',
            'admission_guidelines', 'scholarship_information', 'network_institutes', 'levels', 'programs', 'institute_personnels')
