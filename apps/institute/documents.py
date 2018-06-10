from django_elasticsearch_dsl import DocType, Index, fields, GeoPointField

from ..program.models import Board
from .models import Institute

institute = Index('institutes')

institute.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@institute.doc_type
class InstituteDoc(DocType):
    # TODO Add html-strip analyzer
    description = fields.TextField()
    logo_set = fields.ObjectField()
    coordinate = GeoPointField(attr='coordinate')
    boards = fields.NestedField(properties={
        'slug': fields.TextField(),
        'name': fields.TextField(),
    })
    is_community = fields.KeywordField()
    level = fields.KeywordField(fields={'raw': fields.ListField(fields.StringField(analyzer='keyword'))})

    type = fields.KeywordField(fields={'raw': fields.StringField(analyzer='keyword')})
    district = fields.KeywordField(fields={'raw': fields.StringField(analyzer='keyword')})
    membership = fields.KeywordField(fields={'raw': fields.StringField(analyzer='keyword')})

    affiliation = fields.KeywordField(fields={'raw': fields.ListField(fields.StringField(analyzer='keyword'))})

    def prepare_logo_set(self, instance):
        return instance.logo_set

    def prepare_level(self, instance):
        return list(instance.levels)

    def prepare_is_community(self, instance):
        return instance.type == 'Community'

    def prepare_affiliation(self, instance):
        international = False
        national = False
        for board in instance.boards.all():
            if board.international:
                international = True
            else:
                national = True
        affiliation = []
        if international:
            affiliation.append('International University')
        if national:
            affiliation.append('National Board/University')
        return affiliation

    def get_queryset(self):
        return Institute.objects.filter(published=True).prefetch_related('boards', 'programs')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Board):
            return related_instance.institutes.all()

    class Meta:
        model = Institute
        related_models = [Board]

        fields = [
            'slug', 'name', 'short_name', 'address', 'ugc_accreditation', 'verified', 'featured']
