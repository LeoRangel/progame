from rest_framework import serializers
from progame.models import Turma, Modulo, Questao, Alternativa, Resposta
from ausers.models import Aluno
from django.contrib.auth import get_user_model

from sistema.settings import MEDIA_DE_APROVACAO

User = get_user_model()


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = '__all__'


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        fields = '__all__'


class QuizSerializer(serializers.Serializer):
    media_min_de_aprovacao = serializers.SerializerMethodField()
    turma = TurmaSerializer()
    modulo = ModuloSerializer()

    def get_media_min_de_aprovacao(self, obj):
        media_min_de_aprovacao = int(MEDIA_DE_APROVACAO * 100)
        return str(media_min_de_aprovacao) + "%"


class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = '__all__'


class QuestaoSerializer(serializers.ModelSerializer):
    alternativas = AlternativaSerializer(many=True, read_only=True)
    tempo_para_responder = serializers.SerializerMethodField()
    
    class Meta:
        model = Questao
        fields = '__all__'

    def get_tempo_para_responder(self, obj):
        return obj.tempo_para_responder.total_seconds()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', ]


class AlunoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Aluno
        fields = ['id', 'user']


class RespostaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resposta
        fields = '__all__'
