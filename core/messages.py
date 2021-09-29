from django.contrib import messages


def display_conquista_message(request, conquista_pk):
    """
    Retorna uma message tipo INFO para o template, que é lidada como uma conquista
    A message contém a pk da conquista que será mostrada para o aluno
    """
    messages.add_message(request, messages.INFO, conquista_pk)


def message_created_generic(request):
    messages.add_message(request, messages.SUCCESS, 'Registro cadastrado')


def message_updated_generic(request):
    messages.add_message(request, messages.SUCCESS, 'Registro atualizado')


def message_deleted_generic(request):
    messages.add_message(request, messages.SUCCESS, 'Registro excluído')


def message_success_generic(request):
    messages.add_message(request, messages.SUCCESS, 'Operação realizada')


def message_error_generic(request):
    messages.add_message(request, messages.ERROR, 'Operação não realizada')


def message_success_custom(request, msg):
    messages.add_message(request, messages.SUCCESS, msg)


def message_deleted_custom(request, msg):
    messages.add_message(request, messages.SUCCESS, msg)


def message_error_custom(request, msg):
    messages.add_message(request, messages.ERROR, msg)


def message_info_custom(request, msg):
    messages.add_message(request, messages.INFO, msg)

