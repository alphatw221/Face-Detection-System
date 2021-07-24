from tkinter.constants import BOTH, E, LEFT, X, Y
from tkinter.messagebox import showinfo
import tkinter as tk
from PIL import Image,ImageTk
import cv2
import requests
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import torch


class EmbeddingPage(tk.Frame):
    def __init__(self,parent,application):
        tk.Frame.__init__(self,parent)
        self.grid()

        self.application=application
        self._createWidgets()
        
        self.newFace=None
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
        starCamBtn.pack(side=LEFT,padx=20)
        snapshotBtn = tk.Button(rowFrame1,text="拍照",height=20,width=60,command=self._snapshot)
        snapshotBtn.pack(side=LEFT,padx=20)

        

        self.avatar=tk.Label(dataFrame,border=1)
        self.avatar.pack()

        nameLabel = tk.Label(dataFrame,text="姓名:")
        nameLabel.pack()
        self.nameVar=tk.StringVar()
        nameEntry = tk.Entry(dataFrame,width=20,textvariable=self.nameVar)
        nameEntry.pack()

        rowFrame2=tk.Frame(dataFrame,height=150,width=800)
        rowFrame2.pack(pady=10,ipadx=50)
        rowFrame2.pack_propagate(0)

        deleteBtn = tk.Button(rowFrame2,text="刪除",height=10,width=20,command=None)
        deleteBtn.grid(row=0,column=0,padx=10)
        updateBtn=tk.Button(rowFrame2,text="更新",height=10,width=20,command=self._saveEmbedding)
        updateBtn.grid(row=0,column=1,padx=10)
        


        self.listbox = tk.Listbox(dataFrame,height=30,width=30)
        self.listbox.insert(1,"test")
        self.listbox.pack()

    def _saveEmbedding(self):
        if self.newFace is not None:
            embedding=self.application.resnet(self.newFace.unsqueeze(0))

            self.application.embeddingArray=torch.cat((self.application.embeddingArray,embedding),0)if self.application.embeddingArray is not None else embedding
            torch.save(self.application.embeddingArray,'embeddingArray.pt')

            with open("nameArray.txt", "w") as f:
                f.write(self.nameVar.get() +"\n")
            

    def _startStreaming(self):
        self.isStreaming=True
        self._stream()

    def _snapshot(self):
        success, frame = self.application.cap.read()
        if success:
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            face=self.application.mtcnn(frame)

            if face is not None:
                self.newFace=face
                im_rgb=face.permute(1, 2, 0).numpy().astype(np.uint8)
                im_pil = Image.fromarray(im_rgb)
                imgTK = ImageTk.PhotoImage(image=im_pil)
                self.avatar.configure(image=imgTK)
                self.avatar.image=imgTK

    def _stream(self):
        if self.isStreaming:
            success, frame =self.application.cap.read()
            if success:
                im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(im_rgb)
                imgTK = ImageTk.PhotoImage(image=im_pil)
                self.cameraView.configure(image=imgTK)
                self.cameraView.image=imgTK

            self.cameraView.after(100,lambda:self._stream())