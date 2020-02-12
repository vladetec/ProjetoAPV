from django.contrib import admin
#from django.contrib.admin import ModelAdmin, register
from .models import (
    Doador,
    Operador,
    Entregador,
    Endereco,
    Telefone,
    Email,
    PessoaFisica,
    PessoaJuridica,
    Pessoa,
    Cobranca


)
"""
@register(Pessoa)
    class MaterialPersonAdmin(ModelAdmin):
        icon_name = 'pessoa'
"""		
#admin.site.register(Pessoa)
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'tipo_pessoa', 'endereco_padrao', 'telefone_padrao', 
        'email_padrao', 'data_criacao', 'data_edicao', 'criado_por',
        )
    search_fields = ('nome',)
    list_filter = ('data_criacao',)


admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)
#admin.site.register(Doador)
@admin.register(Doador)
class DoadorAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'endereco_padrao', 'telefone_padrao', 
        'email_padrao', 'lista',
        )
    search_fields = ('nome',)
    list_filter = ('lista',)
#admin.site.register(Operador)
@admin.register(Operador)
class OperadorAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'endereco_padrao', 'telefone_padrao', 
        'email_padrao', 
        )
    search_fields = ('nome',)
    list_filter = ('data_criacao',)
#admin.site.register(Entregador)
@admin.register(Entregador)
class EntregadorAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'endereco_padrao', 'telefone_padrao', 
        'email_padrao', 
        )
    search_fields = ('nome',)
    list_filter = ('data_criacao',)
admin.site.register(Endereco)
admin.site.register(Telefone)
admin.site.register(Email)
#admin.site.register(Cobranca)
@admin.register(Cobranca)
class CobrancaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_barras', 'doador', 'valor', 
        'tipo', 'operador', 'entregador',
        )
    search_fields = ('doador',)
    list_filter = ('tipo', 'operador', 'entregador',)