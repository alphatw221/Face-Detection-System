from tkinter.constants import BOTH, E, LEFT, X, Y
from tkinter.messagebox import showinfo
import tkinter as tk
from PIL import Image,ImageTk
import cv2
import requests
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import torch

class IdentificationPage(tk.Frame):
    def __init__(self,parent,application):
        tk.Frame.__init__(self,parent,)
        self.grid()

        self.application=application
        self._createWidgets()
        
        self.isStreaming=False

    def _createWidgets(self):
        cameraFrame=tk.Frame(self,height=1000,width=800)
        cameraFrame.pack(side=LEFT)
        cameraFrame.pack_propagate(0)

        

        dataFrame=tk.Frame(self,height=1000,width=800)
        dataFrame.pack(side=LEFT)
        dataFrame.pack_propagate(0)


        self.cameraView = tk.Label(cameraFrame)
        self.cameraView.pack(pady=40)
        self.cameraView.pack_propagate(0)

        rowFrame1=tk.Frame(cameraFrame,height=150,width=800)
        rowFrame1.pack(pady=10,ipadx=50)
        rowFrame1.pack_propagate(0)

        starCamBtn=tk.Button(rowFrame1,text="開啟攝影機",height=20,width=60,command=self._startStreaming)
        starCamBtn.pack()

        self.avatar=tk.Label(dataFrame,border=1)
        self.avatar.pack()

        self.nameLabel = tk.Label(dataFrame,text="姓名:")
        self.nameLabel.pack()
        
    def _startStreaming(self):
        self.isStreaming=True
        self._stream()

    def _stream(self):
        if self.isStreaming:
            success, frame =self.application.cap.read()
            if success:
                face=self.application.mtcnn(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                if face is not None:
                    embedding=self.application.resnet(face.unsqueeze(0))
                    self._identify(embedding)
                    im_pil = Image.fromarray(face.permute(1, 2, 0).numpy().astype(np.uint8))
                    imgTK = ImageTk.PhotoImage(image=im_pil)
                    self.cameraView.configure(image=imgTK)
                    self.cameraView.image=imgTK
            self.cameraView.after(20,self._stream)
    
    def _identify(self,embedding):
        tmp=embedding.repeat(self.application.embeddingArray.shape[0],1)
        sorted,indices=torch.sort(torch.sum((tmp-self.application.embeddingArray)**2,1) ,0,)
        self.nameLabel["text"]=self.application.nameArray[indices[0]] if sorted[0]<0.2 else "未知身分"