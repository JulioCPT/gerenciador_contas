import pymongo
from bson import ObjectId

class ContaModel:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="conta_db", collection_name="contas"):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def adicionar_conta(self, conta):
        self.collection.insert_one(conta)

    def listar_contas(self):
        return list(self.collection.find())

    def atualizar_conta(self, conta_id, novos_dados):
        self.collection.update_one({'_id': ObjectId(conta_id)}, {'$set': novos_dados})

    def buscar_conta(self, conta_id):
        return self.collection.find_one({'_id': ObjectId(conta_id)})
    

    def atualizar_conta(self, conta_id, novos_dados):
        
        self.collection.update_one(
            {"_id": ObjectId(conta_id)},
            {"$set": novos_dados}
        )

    def excluir_conta(self, conta_id):
        self.collection.delete_one({'_id': ObjectId(conta_id)})