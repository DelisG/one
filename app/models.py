from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome} - {self.idade} - {self.email}"

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return f"{self.nome} - {self.cpf}"
