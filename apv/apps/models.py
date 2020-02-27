# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.formats import number_format
import re
from django.db import models
from django.utils import timezone
from decimal import Decimal

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
    data_criacao = models.DateTimeField('criado em', auto_now_add=True, auto_now=False, editable=False)
    data_edicao = models.DateTimeField('modificado em', auto_now_add=False, auto_now=True)

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
		
	# clica no doador e retorna os detalhes dela
    def pega_doador_url(self):
        return "/doador/%i" % self.id

    # clica em doaçao e retorna as doaçoes do doador
    def pega_doacao_doador_url(self):
        return "/doacao/?doador=%i" % self.id

    # doaçao por doador
    def pega_doacao_count(self):
        return self.doador_doacao.count()	

class Operador(Pessoa):
    ativo = models.BooleanField('ativo', default=True)
    comissionado = models.BooleanField('comissionado', default=True)
    comissao = models.DecimalField(
        'comissão', max_digits=6, decimal_places=2, default=0.01, blank=True)
    class Meta:
        db_table = 'operador'
        verbose_name = "Operador"
        verbose_name_plural = "operadores"
		
    # clica no operador e retorna os detalhes dela
    def pega_operador_url(self):
        return "/operador/%i" % self.id

    # clica em doaçao e retorna as doaçoes do operador
    def pega_doacao_operador_url(self):
        return "/doacao/?operador=%i" % self.id

    # doaçao por operador
    def pega_doacao_count(self):
        return self.operador_doacao.count()
	
    # comissão operador	
    def pega_comissao(self):
        return "%s" % number_format(self.commissao * 100, 0)

		
class Entregador(Pessoa):
    ativo = models.BooleanField('ativo', default=True)
    comissionado = models.BooleanField('comissionado', default=True)
    comissao = models.DecimalField(
        'comissão', max_digits=6, decimal_places=2, default=0.01, blank=True)
    class Meta:
        db_table = 'entregador'
        verbose_name = "Entregador"
        verbose_name_plural = "Entregadores"
	
	# clica no entregador retorna os detalhes dela
    def pega_entregador_url(self):
        return "/operador/%i" % self.id

    # clica em doaçao e retorna as doaçoes do entregador
    def pega_doacao_operador_url(self):
        return "/doacao/?entregador=%i" % self.id

    # doaçao por entregador
    def pega_doacao_count(self):
        return self.entregador_doacao.count()
	
    # comissão entregador	
    def pega_comissao(self):
        return "%s" % number_format(self.commissao * 100, 0)


class Endereco(models.Model):
    #pessoa_end = models.ForeignKey(
        #Pessoa, related_name="endereco", on_delete=models.CASCADE)
    logradouro = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=16, null=True, blank=True)
    bairro = models.CharField(max_length=64, null=True, blank=True)
    complemento = models.CharField(max_length=64, null=True, blank=True)
    municipio = models.CharField(max_length=64, null=True, blank=True)
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
    email = models.EmailField(max_length=200)

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



"""class Cobranca(TimeStampedModel):
    doador = models.ForeignKey(Doador, on_delete=models.CASCADE, blank=True)
    codigo_barras = models.PositiveIntegerField('código_barras', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        if self.nf:
            return '{} - {} - {}'.format(self.pk, self.nf, self.created.strftime('%d-%m-%Y'))
        return '{} --- {}'.format(self.pk, self.created.strftime('%d-%m-%Y'))

    def nf_formated(self):
        if self.nf:
            return str(self.nf).zfill(3)
        return '---'

"""
class Cobranca(models.Model):
    # Dados	
    #Doador
    doador = models.ForeignKey(
        'apps.Doador', related_name="cobranca_doador", on_delete=models.CASCADE, blank=True, null=True)
    # Operador
    operador = models.ForeignKey(
        'apps.Operador', related_name="cobranca_operador", on_delete=models.CASCADE, blank=True, null=True)
	# Entregador
    entregador = models.ForeignKey(
        'apps.Entregador', related_name="cobranca_entregador", on_delete=models.CASCADE, blank=True, null=True)
    valor_cobranca = models.DecimalField(
	    max_digits=7, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)	
    tipo = models.CharField(
        max_length=1, choices=TIPO_RECIBO, default='1')
	
    # Sobre o objeto
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField('criado em', auto_now_add=True, auto_now=False, editable=False)
    data_edicao = models.DateTimeField('modificado em', auto_now_add=False, auto_now=True)
    

    class Meta:
        ordering = ('pk',)
        verbose_name = "Cobranca"
        db_table = 'cobranca'	
        verbose_name_plural = "Cobrancas"

    def __str__(self):
        return "%03d" % self.id + "/%s" % self.data_criacao.strftime('%y')
    codigo = property(__str__)
	
    def get_detalhe(self):
        return "/cobranca/%i" % self.id

    def valor_cobranca_formated(self):
        return "R$ %s" % number_format(self.valor_cobranca, 2)
    



    

	