class Face:
    def __init__(self,individualId,embedding=None,photo=None):
        self.id=None
        self.individualId=individualId
        self.photo=photo
        self.embedding=embedding
    
    def save(self):
        pass

    def updatae(self,name):
        pass
    
    def delete(self):
        pass 

    @staticmethod
    def get(id):
        pass