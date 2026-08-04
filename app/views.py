from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Aluno, Professor
from .serializers import AlunoSerializer, ProfessorSerializer


def home(request):
    contexto = {
        'alunos': Aluno.objects.all(),
        'professores': Professor.objects.all(),
    }
    return render(request, 'home.html', contexto)

@api_view(['GET'])
def api_alunos(request):
    alunos = Aluno.objects.all()
    serializer = AlunoSerializer(alunos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_professores(request):
    professores = Professor.objects.all()
    serializer = ProfessorSerializer(professores, many=True)
    return Response(serializer.data)
