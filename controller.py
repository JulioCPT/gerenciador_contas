from bson import ObjectId
from model import ContaModel

class ContaController:
    def __init__(self):
        self.model = ContaModel()

    def adicionar_conta(self, tipo, email, senha):
        conta = {
            "tipo": tipo,
            "email": email,
            "senha": senha
        }
        self.model.adicionar_conta(conta)

    def obter_contas(self):
        return self.model.listar_contas()

    def copiar_email(self, conta_id):
        conta = self.model.buscar_conta(conta_id)
        return conta['email']

    def copiar_senha(self, conta_id):
        conta = self.model.buscar_conta(conta_id)
        return conta['senha']
    
    def buscar_conta(self, conta_id):
        return self.model.buscar_conta(conta_id)
    
    def atualizar_conta(self, conta_id, novos_dados):
        self.model.atualizar_conta(conta_id, novos_dados)
    
    def excluir_conta(self, conta_id):
        self.model.excluir_conta(conta_id)
        