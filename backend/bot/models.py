from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, unique=True)
    setor = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"

class Atendimento(models.Model):
    ESTAGIOS = [
        ('INICIO', 'Início'),
        ('MENU_PRINCIPAL', 'Menu Principal'),
        ('AGUARDANDO_DETALHES', 'Aguardando Detalhes'),
        ('AGUARDANDO_ATENDENTE', 'Aguardando Atendente'),
        ('FINALIZADO', 'Finalizado'),
    ]

    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    estagio = models.CharField(max_length=50, choices=ESTAGIOS, default='INICIO')
    setor_escolhido = models.CharField(max_length=50, blank=True, null=True)
    protocolo = models.CharField(max_length=50, blank=True, null=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.colaborador.nome} - {self.estagio}"