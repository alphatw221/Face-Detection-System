import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

from facenet_pytorch import MTCNN, InceptionResnetV1


def main():

    # mtcnn = MTCNN(margin=40, select_largest=False, post_process=False, device='cuda:0')
    # resnet = InceptionResnetV1(pretrained='vggface2').eval()

    cap = cv2.VideoCapture("rtsp://.....")

    while(True):

        success, frame = cap.read()

        if success:

            cv2.imshow("frame",frame)
            # frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            # faces=mtcnn(frame)


            # if faces is not None:
            #     cv2.imshow('frame',cv2.cvtColor(faces.permute(1, 2, 0).numpy().astype(np.uint8),cv2.COLOR_BGR2RGB))
            #     embedding=resnet(faces.unsqueeze(0))
            #     print(embedding.shape)
            #     break
            # for face in faces:
            #     plt.figure("face")
            #     plt.imshow(face.permute(1, 2, 0).int().numpy())
            #     plt.show()

            # cv2.imshow('frame',face.permute(1, 2, 0).int().numpy())
            # plt.imshow(face.permute(1, 2, 0).int().numpy())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()


if __name__ =="__main__":
    main()