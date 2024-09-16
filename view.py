import flet as ft
from controller import ContaController

class ContaView:
    def __init__(self):
        self.controller = ContaController()
        self.page = None

    def construir_pagina_principal(self, page):
        self.page = page
        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(name="settings", color="#c1c1c1", size=60),
                                    ft.Text("Gerenciador de contas", color="#f1a2a2", size=40, weight=ft.FontWeight.BOLD)
                                ],
                                alignment=ft.MainAxisAlignment.START
                            ),
                            padding=ft.padding.only(left=150, top=50),
                            expand=True  
                        ),
                        ft.Container(
                            content=ft.Text("Lista de contas:", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=20),
                            padding=ft.padding.only(right=540, top=50, bottom=10),
                            expand=True  
                        ),
                        ft.Column(self.lista_contas(), alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row([
                            ft.Text("Deseja adicionar uma conta?\nClique no ícone ao lado:", color=ft.colors.WHITE),
                            ft.IconButton(icon=ft.icons.ADD, icon_size=40, on_click=self.adicionar_nova_conta)
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True  
                ),
                expand=True
            )
        )

    def lista_contas(self):
        contas = self.controller.obter_contas()
        grid = []

        for conta in contas:
            id_conta = conta['_id']
            grid.append(
                ft.Row(
                    controls=[
                        # Ícone da pessoa ao lado das informações da conta
                        ft.IconButton(
                            icon=ft.icons.PERSON,
                            on_click=lambda e, id=id_conta: self.abrir_detalhes_conta(id),
                            icon_size=40,  
                            width=80,  
                            height=80,  
                            tooltip="Detalhes da Conta"
                        ),
                        # Informações da conta (tipo e email)
                        ft.Column(
                            controls=[
                                ft.Text(conta['tipo'], color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, size=18),
                                ft.Text(conta['email'], color=ft.colors.GREY)
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        # Ícones de copiar email e senha
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EMAIL,
                                    on_click=lambda e, id=id_conta: self.copiar_email(id),
                                    icon_size=30,  
                                    width=60,  
                                    height=60,  
                                    tooltip="Copiar Email"
                                ),
                                ft.IconButton(
                                    icon=ft.icons.KEY,
                                    on_click=lambda e, id=id_conta: self.copiar_senha(id),
                                    icon_size=30,  
                                    width=60,  
                                    height=60,  
                                    tooltip="Copiar Senha"
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Alinhar ao início
                    expand=True
                )
            )

        return grid
            

       
    
    def copiar_email(self, conta_id):
        email = self.controller.copiar_email(conta_id)
        self.page.set_clipboard(email)

    def copiar_senha(self, conta_id):
        senha = self.controller.copiar_senha(conta_id)
        self.page.set_clipboard(senha)

    

    
    def abrir_detalhes_conta(self, conta_id):
        conta = self.controller.buscar_conta(conta_id)

        tipo_input = ft.Ref[ft.TextField]()
        email_input = ft.Ref[ft.TextField]()
        senha_input = ft.Ref[ft.TextField]()
        editar_btn_ref = ft.Ref[ft.ElevatedButton]()
        confirmar_btn_ref = ft.Ref[ft.ElevatedButton]()
        deletar_btn_ref = ft.Ref[ft.ElevatedButton]()

        def habilitar_edicao(e):
            tipo_input.current.read_only = False
            email_input.current.read_only = False
            senha_input.current.read_only = False
            senha_input.current.password = False
            confirmar_btn_ref.current.visible = True
            deletar_btn_ref.current.visible = True
            editar_btn_ref.current.visible = False
            self.page.update()

        def confirmar_alteracoes(e):
            tipo = tipo_input.current.value
            email = email_input.current.value
            senha = senha_input.current.value
            if tipo and email and senha:
                novos_dados = {
                    "tipo": tipo,
                    "email": email,
                    "senha": senha
                }
                self.controller.atualizar_conta(conta_id, novos_dados)
                self.page.dialog.open = False
                self.page.update()
                self.atualizar_lista()

        def deletar_conta(e):
            self.controller.excluir_conta(conta_id)
            self.page.dialog.open = False
            self.page.update()
            self.atualizar_lista()

        def fechar_popup(e):
            self.page.dialog.open = False
            self.page.update()

        popup = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            icon_size=30,
                            on_click=fechar_popup,
                            tooltip="Fechar"
                        )
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Row([
                        ft.Icon(name="person", color=ft.colors.WHITE),
                        ft.Text("Detalhes da conta", color=ft.colors.WHITE, size=25)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.TextField(label="Conta", ref=tipo_input, value=conta['tipo'], read_only=True),  
                    ft.TextField(label="Email", ref=email_input, value=conta['email'], read_only=True),  
                    ft.TextField(label="Senha", password=True, ref=senha_input, value=conta['senha'], read_only=True),  
                    ft.Row([
                        ft.ElevatedButton("Editar", ref=editar_btn_ref, on_click=habilitar_edicao, color=ft.colors.BLACK, bgcolor=ft.colors.LIGHT_BLUE_400),
                        ft.ElevatedButton("Deletar", ref=deletar_btn_ref, on_click=deletar_conta, color=ft.colors.BLACK, bgcolor=ft.colors.RED, visible=False),
                        ft.ElevatedButton("Confirmar", ref=confirmar_btn_ref, on_click=confirmar_alteracoes, color=ft.colors.BLACK, bgcolor=ft.colors.GREEN, visible=False)
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                ], alignment=ft.MainAxisAlignment.CENTER),
                height=300,
            )
        )

        self.page.dialog = popup
        self.page.dialog.open = True
        self.page.update()

   
    def adicionar_nova_conta(self, e=None):
       
        tipo_input = ft.Ref[ft.TextField]()
        email_input = ft.Ref[ft.TextField]()
        senha_input = ft.Ref[ft.TextField]()
        
        def confirmar(e):
            tipo = tipo_input.current.value
            email = email_input.current.value
            senha = senha_input.current.value
            if tipo and email and senha:
                
                self.controller.adicionar_conta(tipo, email, senha)
                self.page.dialog.open = False  
                self.page.update()
                self.atualizar_lista()  

        def limpar(e):
            tipo_input.current.value = ""
            email_input.current.value = ""
            senha_input.current.value = ""
            self.page.update()
        
        def fechar_popup(e):
            self.page.dialog.open = False
            self.page.update()

        
        popup = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            icon_size=30,
                            on_click=fechar_popup,
                            tooltip="Fechar"
                        )
                    ], alignment=ft.MainAxisAlignment.END),
                    ft.Row([
                        ft.Icon(name="person", color=ft.colors.WHITE),
                        ft.Text("Adicionar conta", color=ft.colors.WHITE, size=25)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.TextField(label="Conta", ref=tipo_input),
                    ft.TextField(label="Email", ref=email_input),
                    ft.TextField(label="Senha", password=False, ref=senha_input),
                    ft.Row([
                        ft.ElevatedButton("Limpar", on_click=limpar, color=ft.colors.BLACK, bgcolor=ft.colors.LIGHT_BLUE_400),
                        ft.ElevatedButton("Confirmar", on_click=confirmar, color=ft.colors.BLACK, bgcolor=ft.colors.GREEN)
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                ], alignment=ft.MainAxisAlignment.CENTER),
                height=300,
            )
        )

        self.page.dialog = popup
        self.page.dialog.open = True
        self.page.update()

    def atualizar_lista(self):
        
        self.page.controls.clear()
        
        
        self.construir_pagina_principal(self.page)
        
        
        self.page.update()
        