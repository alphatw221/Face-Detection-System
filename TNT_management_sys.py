from page.IdentificationPage import IdentificationPage
from page.EmbeddingPage import EmbeddingPage
from page.ConsolePage import ConsolePage
from tkinter import ttk
from tkinter.constants import BOTH, E, LEFT, X, Y
from tkinter.messagebox import showinfo
import tkinter as tk
import sys
from PIL import Image,ImageTk
import cv2
import requests
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import torch

class Application(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames={}
        self.isFullScreen=False
        self.bind('<F12>',self._toggle_fullScreen)

        self._createWidgets()
    def _createWidgets(self):
        navbar=tk.Frame(self,height=60)
        navbar.pack(fill=X)
        navbar.pack_propagate(0)
        container=tk.Frame(self)
        container.pack( fill="both", expand = True,)

        self.consolePageBtn = tk.Button(navbar,text="控制頁",command=lambda:self.show_frame(ConsolePage))
        self.consolePageBtn.pack(side=LEFT,fill=Y)

        self.embeddingPageBtn = tk.Button(navbar,text="特徵管理",command=lambda:self.show_frame(EmbeddingPage))
        self.embeddingPageBtn.pack(side=LEFT,fill=Y)

        self.Page3Btn = tk.Button(navbar,text="身分識別",command=lambda:self.show_frame(IdentificationPage))
        self.Page3Btn.pack(side=LEFT,fill=Y)

        self.Page4Btn = tk.Button(navbar,text="第四頁",command=None)
        self.Page4Btn.pack(side=LEFT,fill=Y)

        self.cap = cv2.VideoCapture(0)  
        self.mtcnn = MTCNN(margin=40, select_largest=False, post_process=False, device='cuda:0')
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

        for F in (ConsolePage, EmbeddingPage, IdentificationPage):
            frame = F(container,self)
            self.frames[F]=frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ConsolePage)


    def _startupProcess(self):
        #fetch data
        try:
            self.embeddingArray=torch.load('embeddingArray.pt')
        except:
            self.embeddingArray=None

        self.nameArray=[]
        with open("nameArray.txt", "r",encoding="utf-8") as f:
            for line in f.readlines():
                self.nameArray.append(line)
        #fetch model
        #fetch camera
        pass

    def _toggle_fullScreen(self, event):
        
        is_windows = lambda : 1 if sys.platform.startswith('win32') else 0

        self.isFullScreen = not self.isFullScreen
        self.attributes("-fullscreen" if is_windows() else "-zoomed", self.isFullScreen)

    def show_frame(self,F):
        frame=self.frames[F]
        frame.tkraise()



def main():
    application=Application()
    application.title('TNT Management')
    # application.iconbitmap('')
    application.geometry("1600x1000")

    application.mainloop()

if __name__=="__main__":
    main()