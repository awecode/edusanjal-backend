from django_elasticsearch_dsl import DocType, Index, fields, GeoPointField

from .models import Institute

institute = Index('institutes')

institute.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@institute.doc_type
class InstituteDoc(DocType):
    description = fields.TextField()
    logo_set = fields.ObjectField(attr='logo_set')
    coordinate = GeoPointField(attr='coordinate')
    boards = fields.NestedField(properties={
        'slug': fields.TextField(),
        'name': fields.TextField(),
    })

    class Meta:
        model = Institute

        fields = [
            'slug', 'name', 'short_name', 'address', 'district', 'ugc_accreditation', 'verified', 'type'
        ]
