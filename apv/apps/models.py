# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
import re
from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.urls import reverse_lazy

TIPO_TELEFONE = [
    ('FIX', "Fixo"),
    ('CEL', "Celular"),
    ('OUT', "Outro"),
]

TIPO_DOADOR = [
    ('CANCELADO', "Cancelado"),
    ('FIDELIZADO', "Fidelizado"),
    ('MENSALISTA', "Mensalista"),
    ('ESPERA_DIA', "Espera_dia"),
    ('EX_FIDELIZADO', "Ex_fidelizado"),
]
TIPO_RECIBO = [
    ('1', "Recebido"),
    ('2', "Confirmado"),
    ('3', "Pre_datado"),
    ('4', "Saldo"),
    ('5', "Dia_seguinte"),
	('6', "Retornado"),
]

UF_SIGLA = [
    ('AC', 'AC'),
    ('AL', 'AL'),
    ('AP', 'AP'),
    ('AM', 'AM'),
    ('BA', 'BA'),
    ('CE', 'CE'),
    ('DF', 'DF'),
    ('ES', 'ES'),
    ('EX', 'EX'),
    ('GO', 'GO'),
    ('MA', 'MA'),
    ('MT', 'MT'),
    ('MS', 'MS'),
    ('MG', 'MG'),
    ('PA', 'PA'),
    ('PB', 'PB'),
    ('PR', 'PR'),
    ('PE', 'PE'),
    ('PI', 'PI'),
    ('RJ', 'RJ'),
    ('RN', 'RN'),
    ('RS', 'RS'),
    ('RO', 'RO'),
    ('RR', 'RR'),
    ('SC', 'SC'),
    ('SP', 'SP'),
    ('SE', 'SE'),
    ('TO', 'TO'),
]

COD_UF = [
    ('12', 'AC'),
    ('27', 'AL'),
    ('16', 'AP'),
    ('13', 'AM'),
    ('29', 'BA'),
    ('23', 'CE'),
    ('53', 'DF'),
    ('32', 'ES'),
    ('EX', 'EX'),
    ('52', 'GO'),
    ('21', 'MA'),
    ('51', 'MT'),
    ('50', 'MS'),
    ('31', 'MG'),
    ('15', 'PA'),
    ('25', 'PB'),
    ('41', 'PR'),
    ('26', 'PE'),
    ('22', 'PI'),
    ('33', 'RJ'),
    ('24', 'RN'),
    ('43', 'RS'),
    ('11', 'RO'),
    ('14', 'RR'),
    ('42', 'SC'),
    ('35', 'SP'),
    ('28', 'SE'),
    ('17', 'TO'),
]

TIPO_PESSOA = [
    ('PF', 'Pessoa Física'),
    ('PJ', 'Pessoa Jurídica'),
]

MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        abstract = True
		

class Pessoa(models.Model):
    # Dados
    nome = models.CharField(max_length=255)
    tipo_pessoa = models.CharField(max_length=2, choices=TIPO_PESSOA)

    # Dados padrao
    endereco_padrao = models.ForeignKey(
        'apps.Endereco', related_name="endereco_pe", on_delete=models.CASCADE, null=True, blank=True)
    telefone_padrao = models.ForeignKey(
        'apps.Telefone', related_name="telefone_pe", on_delete=models.CASCADE, null=True, blank=True)
    email_padrao = models.ForeignKey(
        'apps.Email', related_name="email_pe", on_delete=models.CASCADE, null=True, blank=True)

    # Sobre o objeto
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(editable=False)
    data_edicao = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Atualizar datas criacao edicao
        if not self.data_criacao:
            self.data_criacao = timezone.now()
        self.data_edicao = timezone.now()
        return super(Pessoa, self).save(*args, **kwargs)

    @property
    def cpf_cnpj_apenas_digitos(self):
        if self.tipo_pessoa == 'PF':
            if self.pessoa_fis_info.cpf:
                return re.sub('[./-]', '', self.pessoa_fis_info.cpf)

        elif self.tipo_pessoa == 'PJ':
            if self.pessoa_jur_info.cnpj:
                return re.sub('[./-]', '', self.pessoa_jur_info.cnpj)

        else:
            return ''

    @property
    def uf_padrao(self):
        if self.endereco_padrao:
            return self.endereco.uf
        else:
            return ''

    def __unicode__(self):
        s = u'%s' % (self.nome)
        return s

    def __str__(self):
        s = u'%s' % (self.nome)
        return s
class PessoaFisica(models.Model):
    pessoa_id = models.OneToOneField(
        Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='pessoa_fis_info')
    cpf = models.CharField(max_length=32, null=True, blank=True)
    rg = models.CharField(max_length=32, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)

    @property
    def format_cpf(self):
        if self.cpf:
            return 'CPF: {}'.format(self.cpf)
        else:
            return ''

    @property
    def format_rg(self):
        if self.rg:
            return 'RG: {}'.format(self.rg)
        else:
            return ''


class PessoaJuridica(models.Model):
    pessoa_id = models.OneToOneField(
        Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='pessoa_jur_info')
    cnpj = models.CharField(max_length=32, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=255, null=True, blank=True)

    responsavel = models.CharField(max_length=32, null=True, blank=True)


    @property
    def format_cnpj(self):
        if self.cnpj:
            return 'CNPJ: {}'.format(self.cnpj)
        else:
            return ''

    @property
    def format_ie(self):
        if self.inscricao_estadual:
            return 'IE: {}'.format(self.inscricao_estadual)
        else:
            return ''

    @property
    def format_responsavel(self):
        if self.responsavel:
            return 'Representante: {}'.format(self.responsavel)
        else:
            return ''

class Doador(Pessoa):
    lista = models.CharField(max_length=13, choices=TIPO_DOADOR)
    class Meta:
        db_table = 'doador'
        verbose_name = "Doador"
        verbose_name_plural = "Doadores"

class Operador(Pessoa):
    class Meta:
        db_table = 'operador'
        verbose_name = "Operador"
        verbose_name_plural = "operadores"

class Entregador(Pessoa):
    class Meta:
        db_table = 'entregador'
        verbose_name = "Entregador"
        verbose_name_plural = "Entregadores"


class Endereco(models.Model):
    #pessoa_end = models.ForeignKey(
        #Pessoa, related_name="endereco", on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=16, null=True, blank=True)
    bairro = models.CharField(max_length=64, null=True, blank=True)
    complemento = models.CharField(max_length=64, null=True, blank=True)
    municipio = models.CharField(max_length=64, null=True, blank=True)
    cmun = models.CharField(max_length=9, null=True, blank=True)
    cep = models.CharField(max_length=16, null=True, blank=True)
    uf = models.CharField(max_length=3, null=True,
                          blank=True, choices=UF_SIGLA)

    @property
    def format_endereco(self):
        return '{0}, {1} - {2}'.format(self.logradouro, self.numero, self.bairro)

    @property
    def format_endereco_completo(self):
        return '{0} - {1} - {2} - {3} - {4} - {5} - {6}'.format(self.logradouro, self.numero, self.bairro, self.municipio, self.cep, self.uf, self.pais)

    class Meta:
        db_table = 'endereco'
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        #ordering = ('nome',)


    def __unicode__(self):
        s = u'%s, %s, %s (%s)' % (
            self.logradouro, self.numero, self.municipio, self.uf)
        return s

    def __str__(self):
        s = u'%s, %s, %s (%s)' % (
            self.logradouro, self.numero, self.municipio, self.uf)
        return s


class Telefone(models.Model):
    #pessoa_tel = models.ForeignKey(
        #Pessoa, related_name="telefone", on_delete=models.CASCADE)
    tipo_telefone = models.CharField(
        max_length=8, choices=TIPO_TELEFONE, null=True, blank=True)
    telefone = models.CharField(max_length=32)

    def get_telefone_apenas_digitos(self):
        return self.telefone.replace('(', '').replace(' ', '').replace(')', '').replace('-', '')

    class Meta:
        db_table = 'fone'
        verbose_name = "Telefone"
        verbose_name_plural = "Telefones"
        #ordering = ('nome',)

    def __str__(self):
        s = u'%s' % (self.telefone)
        return s

    def __unicode__(self):
        s = u'%s' % (self.telefone)
        return s

class Email(models.Model):
    #pessoa_email = models.ForeignKey(
        #Pessoa, related_name="email", on_delete=models.CASCADE)
    email = models.CharField(max_length=255)

    class Meta:
        db_table = 'email'
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        #ordering = ('nome',)

    class Meta:
        db_table = 'email'
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        #ordering = ('nome',)

    def __str__(self):
        s = u'%s' % (self.email)
        return s

    def __unicode__(self):
        s = u'%s' % (self.email)
        return s
		
		
class Cobranca(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    codigo = models.PositiveIntegerField('código', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.codigo:
            return '{} - {} - {}'.format(self.pk, self.codigo, self.created.strftime('%d-%m-%Y'))
        return '{} --- {}'.format(self.pk, self.created.strftime('%d-%m-%Y'))

    def codigo_formated(self):
        if self.codigo:
            return str(self.codigo).zfill(3)
        return '---'
		
"""		
class CobrancaEntrada(Cobranca):
    objects = CobrancaEntradaManager()

    class Meta:
        proxy = True
        verbose_name = 'cobranca entrada'
        verbose_name_plural = 'cobrancas entrada'


class CobrancaSaida(Cobranca):

    objects = CobrancaSaidaManager()

    class Meta:
        proxy = True
        verbose_name = 'cobranca saída'
        verbose_name_plural = 'cobrancas saída'

		
"""		
class CobrancaItens(models.Model):
    # Dados
    cobranca = models.ForeignKey(
	    Cobranca,
		on_delete=models.CASCADE,
		related_name='cobrancas'
		)
    valor = models.DecimalField(
	    max_digits=7, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
	
	#Doador
    doador = models.ForeignKey(
        'apps.Doador', related_name="cobranca_doador", on_delete=models.CASCADE, blank=True, null=True)
    
	# Operador
    operador = models.ForeignKey(
        'apps.Operador', related_name="cobranca_operador", on_delete=models.CASCADE, blank=True, null=True)
	# Entregador
    entregador = models.ForeignKey(
        'apps.Entregador', related_name="cobranca_entregador", on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(
        max_length=1, choices=TIPO_RECIBO, default='1')
		
	# Sobre o objeto
    #criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #data_criacao = models.DateTimeField(editable=False, null=True, blank=True)
    #data_edicao = models.DateTimeField(null=True, blank=True )

    

    class Meta:
        verbose_name = "CobrancaItens"
        db_table = 'cobranca_iten'	
        verbose_name_plural = "Cobrancas_itens"
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.cobranca.pk, self.doador.nome)


    #def __str__(self):
        #s = u'%s' % (self.codigo_barras+ '-' + self.doador.nome)
        #return s

    #def __unicode__(self):
        #s = u'%s' % (self.codigo_barras+ '-' + self.doador.nome)
        #return s