import re

from rest_framework import serializers

from .models import Aluno, Professor


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'idade', 'email']


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['id', 'nome', 'cpf']

    def validate_cpf(self, value):
        digitos = re.sub(r'\D', '', value)

        if len(digitos) != 11:
            raise serializers.ValidationError('CPF deve ter 11 dígitos.')

        duplicados = Professor.objects.filter(cpf=digitos)
        if self.instance is not None:
            duplicados = duplicados.exclude(pk=self.instance.pk)
        if duplicados.exists():
            raise serializers.ValidationError('Já existe professor com este CPF.')

        return digitos
