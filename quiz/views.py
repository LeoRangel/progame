import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.views import View

from ausers.templatetags.ausers_tags import check_professor
from ausers.utils import ProfessorMixin
from quiz.forms import LinkAjudaForm
from quiz.models import LinkAjuda, Quiz
from django.utils.text import Truncator


def index(request):
    return render(request, 'quiz/index.html')


class GetLinksAjuda(ProfessorMixin, View):

    def test_func(self):
        quiz = get_object_or_404(Quiz, uuid=self.kwargs['uuid'])
        return check_professor(quiz.modulo.turma, self.request)

    def get(self, request, *args, **kwargs):
        quiz = Quiz.objects.get(uuid=self.kwargs['uuid'])

        links = []
        for link in quiz.links_ajuda.order_by('-pk'):
            links.append({
                'id': link.pk,
                'nome': link.nome,
                'url': link.url,
                'nome_trunc': Truncator(link.nome).words(8),
                'url_trunc': Truncator(link.url).chars(45)
            })

        return JsonResponse(links, safe=False)


class LinkAjudaCreateView(ProfessorMixin, CreateView):
    model = LinkAjuda
    form_class = LinkAjudaForm

    def test_func(self):
        quiz = get_object_or_404(Quiz, uuid=self.kwargs['uuid'])
        return check_professor(quiz.modulo.turma, self.request)

    def form_valid(self, form):
        link = form.save()
        quiz = get_object_or_404(Quiz, uuid=self.kwargs['uuid'])
        quiz.links_ajuda.add(link)

        response_data = {
            'id': link.pk,
            'nome': link.nome,
            'url': link.url,
            'nome_trunc': Truncator(link.nome).words(8),
            'url_trunc': Truncator(link.url).chars(45)
        }
        return JsonResponse(response_data, safe=False)

    def form_invalid(self, form):
        res = {'errors': form.errors}

        return HttpResponse(json.dumps(res), status=500)
