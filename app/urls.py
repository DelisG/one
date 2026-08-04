from django.urls import path
from .views import home, api_alunos, api_professores

urlpatterns = [
    path('', home, name='home'),
    path('api/alunos', api_alunos, name='api_alunos'),
    path('api/professores', api_professores, name='api_professores'),
]
