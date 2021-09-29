from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.utils import generate_random_number


@receiver(pre_save, sender=User)
def gerar_username_ao_cadastrar_usuario(sender, instance, *args, **kwargs):
    if not instance.is_superuser:
        primeira_parte_email = str(instance.email.split("@")[0])

        user_exists = True
        while user_exists:
            numero = str(generate_random_number(digits=4))
            try:
                User.objects.get(username__icontains=numero)
            except User.DoesNotExist:
                user_exists = False

        instance.username = primeira_parte_email + '@' + numero
