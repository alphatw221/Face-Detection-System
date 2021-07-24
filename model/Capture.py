class Capture:
    def __init__(self,individualId,cameraId,euclideanScore):
        self.id=None
        self.individualId=individualId
        self.cameraId=cameraId
        self.eculideanScore=euclideanScore
        self.dateTime=None

    def save(self):
        pass

    def updatae(self,name):
        pass
    
    def delete(self):
        pass 

    @staticmethod
    def search(individualId=None,cameraId=None,startTime=None,endTime=None):
        pass