from django.contrib import admin
from jet.admin import CompactInline

from edusanjal.lib.forms import StartEndForm
from .forms import InstituteForm
from apps.program.models import Program
from .models import Institute, Personnel, Designation, Award, InstituteAward, InstitutePersonnel, InstituteProgram, Feature, \
    Membership, Admission, ScholarshipCategory, Scholarship, Rank, Ranking, InstituteImage, InstituteDocument


class InstituteProgramInline(admin.TabularInline):
    model = InstituteProgram
    verbose_name = 'Program'
    verbose_name_plural = 'Programs'


class ImageInline(admin.TabularInline):
    model = InstituteImage
    verbose_name = 'Image'
    verbose_name_plural = 'Images'
    readonly_fields = ('height', 'width')


class DocumentInline(admin.TabularInline):
    model = InstituteDocument
    verbose_name = 'Document'
    verbose_name_plural = 'Documents'


class InstitutePersonnelInline(CompactInline):
    model = InstitutePersonnel
    verbose_name = 'Personnel'
    verbose_name_plural = 'Personnels'


class MembershipInline(admin.TabularInline):
    model = Membership
    verbose_name = 'Membership'
    verbose_name_plural = 'Memberships'
    readonly_fields = ['active', ]
    form = StartEndForm


class FeatureInline(admin.TabularInline):
    model = Feature
    verbose_name = 'Feature'
    verbose_name_plural = 'Features'
    readonly_fields = ['active', ]
    form = StartEndForm


class InstituteAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    list_filter = ['verified', 'is_member', 'featured', 'published', 'boards', 'ugc_accreditation', 'district', 'type']
    list_display = ['name', 'slug', 'verified', 'is_member', 'featured']
    form = InstituteForm
    inlines = [ImageInline, DocumentInline, InstituteProgramInline, InstitutePersonnelInline, MembershipInline, FeatureInline]
    readonly_fields = ['featured', 'is_member']
    exclude = ['images', 'documents']


class AdmissionProgramInline(admin.TabularInline):
    model = Program.admissions.through
    verbose_name = 'Program'
    verbose_name_plural = 'Programs'


class AdmissionInstituteInline(admin.TabularInline):
    model = Institute.admissions.through
    verbose_name = 'Institute'
    verbose_name_plural = 'Institutes'


class AdmissionAdmin(admin.ModelAdmin):
    inlines = [AdmissionProgramInline, AdmissionInstituteInline]
    exclude = ['programs', 'institutes']


class InstituteAwardInline(admin.TabularInline):
    model = InstituteAward
    verbose_name = 'Institute'
    verbose_name_plural = 'Institutes'


class AwardAdmin(admin.ModelAdmin):
    inlines = [InstituteAwardInline, ]


admin.site.register(Institute, InstituteAdmin)

admin.site.register(Personnel)
admin.site.register(Designation)
admin.site.register(Award, AwardAdmin)
admin.site.register(Feature)
admin.site.register(Membership)
admin.site.register(Admission, AdmissionAdmin)
admin.site.register(ScholarshipCategory)
admin.site.register(Scholarship)
admin.site.register(Ranking)
