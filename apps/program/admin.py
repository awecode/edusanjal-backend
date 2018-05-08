from django.contrib import admin
from .models import Board, Faculty, Discipline, Council, Program, CouncilDocument, BoardDocument, BoardImage

admin.site.register(Board)
admin.site.register(BoardDocument)
admin.site.register(BoardImage)
admin.site.register(Faculty)
admin.site.register(Discipline)
admin.site.register(Council)
admin.site.register(CouncilDocument)
admin.site.register(Program)
