from django.contrib import admin

from .models import Institute, Personnel, Designation, Award, InstituteAward, InstitutePersonnel, InstituteProgram, Feature, \
    Membership, Admission, ScholarshipCategory, Scholarship, Rank, Ranking, InstituteImage, InstituteDocument


class ImageInline(admin.TabularInline):
    model = InstituteImage
    verbose_name = 'Image'
    verbose_name_plural = 'Images'


class DocumentInline(admin.TabularInline):
    model = InstituteDocument
    verbose_name = 'Document'
    verbose_name_plural = 'Documents'


class InstituteAdmin(admin.ModelAdmin):
    inlines = [ImageInline, DocumentInline]
    exclude = ['images', 'documents']
    pass


admin.site.register(Institute, InstituteAdmin)

admin.site.register(Personnel)
admin.site.register(Designation)
admin.site.register(Award)
admin.site.register(Feature)
admin.site.register(Membership)
admin.site.register(Admission)
admin.site.register(ScholarshipCategory)
admin.site.register(Scholarship)
admin.site.register(Ranking)
