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
    Cobranca,
	CobrancaItens


)
"""
@register(Pessoa)
    class MaterialPersonAdmin(ModelAdmin):
        icon_name = 'pessoa'
"""		
admin.site.register(Pessoa)
admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)
admin.site.register(Doador)
admin.site.register(Operador)
admin.site.register(Entregador)
admin.site.register(Endereco)
admin.site.register(Telefone)
admin.site.register(Email)
admin.site.register(Cobranca)
admin.site.register(CobrancaItens)