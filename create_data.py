import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apv.settings")
django.setup()

import string
import timeit
from random import choice, random, randint
from apv.apps.models import Doador


class Utils:
    ''' Métodos genéricos. '''
    @staticmethod
    def gen_digits(max_length):
        return str(''.join(choice(string.digits) for i in range(max_length)))


class DoadorClass:

    @staticmethod
    def criar_doadores(doadores):
        Doador.objects.all().delete()
        aux = []
        for doador in doadores:
            data = dict(
                doador=doador,
                lista=choice((TIPO_DOADOR)),
                #valor=Utils.gen_digits(8),
                valor=random() * randint(10, 50),
                telefone=randint(10, 200),
            )
            obj = Doador(**data)
            aux.append(obj)
        Doador.objects.bulk_create(aux)


doadores = (
    'Antonio Barros dos Santos',
    'Amarildo da Silva',
    'Borges Ramos de Andrade',
    'Carlos Eduardo Ramel',
    'Camila Bravanni Ferreira',
    'Dimas Quilharmo Severo',
    'Dorildo das Tabajras',
    'Fabio Jonas do Amaral',
    'Fabiolla Sobral',
    'Fabianna Kelly',
    'Khristinne Ferras',
    'Rivaldo Araujo',
    'Quirvaldo Perereira',
    'Ze Maranhao',
    'Xuxa Meneguel',
    'Ytallo Kumakitaro',
)

tic = timeit.default_timer()

DoadorClass.criar_doadores(doadores)


toc = timeit.default_timer()

print('Tempo:', toc - tic)
