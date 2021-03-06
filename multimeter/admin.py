""" Настройка интерфейса администратора """

from django.contrib import admin
from . import models

admin.site.register(models.CountryReference)
admin.site.register(models.Account)
admin.site.register(models.Contest)
admin.site.register(models.Problem)
admin.site.register(models.ContestProblem)
admin.site.register(models.SubTask)
admin.site.register(models.Language)
admin.site.register(models.Tag)
