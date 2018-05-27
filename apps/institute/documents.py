from django_elasticsearch_dsl import DocType, Index, fields, GeoPointField

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

    def prepare_logo_set(self, instance):
        return instance.logo_set

    def prepare_is_community(self, instance):
        return instance.type == 'Community'

    class Meta:
        model = Institute

        fields = [
            'slug', 'name', 'short_name', 'address', 'district', 'ugc_accreditation', 'verified', 'type', 'featured', 'is_member'
        ]
