import flet as ft
from view import ContaView

def main(page: ft.Page):
    conta_view = ContaView()
    conta_view.construir_pagina_principal(page)

ft.app(target=main)
