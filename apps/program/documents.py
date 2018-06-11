from django_elasticsearch_dsl import DocType, Index, fields, GeoPointField

from .models import Program

program = Index('programs')

program.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@program.doc_type
class ProgramDoc(DocType):
    description = fields.TextField()

    level = fields.KeywordField(fields={'raw': fields.StringField(analyzer='keyword')})
    # discipline = fields.KeywordField(fields={'raw': fields.StringField(analyzer='keyword')})

    def get_queryset(self):
        return Program.objects.filter(published=True)

    class Meta:
        model = Program

        fields = ['slug', 'name', 'full_name', 'short_name']
