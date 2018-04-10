from django.contrib import admin

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


class DocumentInline(admin.TabularInline):
    model = InstituteDocument
    verbose_name = 'Document'
    verbose_name_plural = 'Documents'


class InstituteAdmin(admin.ModelAdmin):
    inlines = [ImageInline, DocumentInline, InstituteProgramInline]
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


admin.site.register(Institute, InstituteAdmin)

admin.site.register(Personnel)
admin.site.register(Designation)
admin.site.register(Award)
admin.site.register(Feature)
admin.site.register(Membership)
admin.site.register(Admission, AdmissionAdmin)
admin.site.register(ScholarshipCategory)
admin.site.register(Scholarship)
admin.site.register(Ranking)
