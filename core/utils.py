import datetime
from random import randint, choice
import base64
import string
from django.core.files.base import ContentFile


def generate_random_number(digits):
    """Gera um número aleatório com a quantidade de dígitos informada"""
    range_start = 10 ** (digits - 1)
    range_end = (10 ** digits) - 1
    return randint(range_start, range_end)


def generate_random_string(size=6, chars=string.ascii_lowercase + string.digits):
    """Gera uma string aleatória com números e letras"""
    return ''.join(choice(chars) for _ in range(size))


def base64_to_file(data):
    """
    Recebe uma string base64 e retorna como arquivo
    Útil para usar com o croppie.js
    """
    format, imgstr = data.split(';base64,')
    ext = '.' + str(format.split('/')[-1])
    name = str(datetime.datetime.today()) + str(generate_random_number(4))

    data = ContentFile(base64.b64decode(imgstr), name=name + ext)
    return data


def arredondar(x, base=1):
    """Arredonda valor"""
    return base * round(x/base)
