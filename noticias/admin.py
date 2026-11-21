
from django.contrib import admin
from .models import (
    Noticia,
    Comentario,
    Leitor,
    SolicitacaoJornalista,
    CertificadoSolicitacao
)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "categoria",
        "regiao",
        "status",
        "data_criacao"
    )
    list_filter = ("status", "categoria", "regiao")
    search_fields = ("titulo", "resumo", "autor_email")
    ordering = ("-data_criacao",)


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "noticia",
        "data_criacao",
        "aprovado"
    )
    list_filter = ("aprovado", "data_criacao")
    search_fields = ("nome", "texto")
    list_editable = ("aprovado",)
    ordering = ("-data_criacao",)


@admin.register(Leitor)
class LeitorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "email",
        "jornalista",
        "data_criacao"
    )
    list_filter = ("jornalista",)
    search_fields = ("nome", "email")


@admin.register(SolicitacaoJornalista)
class SolicitacaoJornalistaAdmin(admin.ModelAdmin):
    list_display = (
        "nome_completo",
        "leitor",
        "cpf",
        "zona",
        "bairro",
        "status",
        "data_criacao"
    )
    list_filter = ("status", "zona")
    search_fields = (
        "nome_completo",
        "cpf",
        "bairro",
        "leitor__nome",
        "leitor__email"
    )
    ordering = ("-data_criacao",)


@admin.register(CertificadoSolicitacao)
class CertificadoSolicitacaoAdmin(admin.ModelAdmin):
    list_display = ("solicitacao", "imagem")
    search_fields = (
        "solicitacao__nome_completo",
        "solicitacao__leitor__email"
    )
