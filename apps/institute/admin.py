from django.contrib import admin

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


class InstitutePersonnelInline(admin.TabularInline):
    model = InstitutePersonnel
    verbose_name = 'Personnel'
    verbose_name_plural = 'Personnels'


class InstituteAdmin(admin.ModelAdmin):
    form = InstituteForm
    inlines = [ImageInline, DocumentInline, InstituteProgramInline, InstitutePersonnelInline]
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
