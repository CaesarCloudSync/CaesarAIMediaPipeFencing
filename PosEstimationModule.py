import cv2
import mediapipe as mp
import time
import math
import dataclasses
import matplotlib.pyplot as plt
from typing import List, Mapping, Optional, Tuple, Union
import json
_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5
_BGR_CHANNELS = 3

WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)
@dataclasses.dataclass
class DrawingSpec:
  # Color for drawing the annotation. Default to the white color.
  color: Tuple[int, int, int] = WHITE_COLOR
  # Thickness for drawing the annotation. Default to 2 pixels.
  thickness: int = 2
  # Circle radius. Default to 2 pixels.
  circle_radius: int = 2

class poseDetector():
    def __init__(self, mode=False, smooth=True, detectionCon=0.5, trackCon=0.5):
 
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.pTime = 0

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                smooth_landmarks=self.smooth,
                                min_detection_confidence=self.detectionCon,
                                min_tracking_confidence=self.trackCon)

    def normalize_color(self,color):
        return tuple(v / 255. for v in color)

    def plot_landmarks(self,count,landmark_list,
                    connections,
                    landmark_drawing_spec: DrawingSpec = DrawingSpec(
                        color=RED_COLOR, thickness=5),
                    connection_drawing_spec: DrawingSpec = DrawingSpec(
                        color=BLACK_COLOR, thickness=5),
                    elevation: int = 10,
                    azimuth: int = 10):
        frame_3d_plot = {"landmarks":[],
                              "connections":[]}
        if not landmark_list:
            return
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection='3d')
        ax.view_init(elev=elevation, azim=azimuth)
        plotted_landmarks = {}
        for idx, landmark in enumerate(landmark_list.landmark):
            if ((landmark.HasField('visibility') and
                landmark.visibility < _VISIBILITY_THRESHOLD) or
                (landmark.HasField('presence') and
                landmark.presence < _PRESENCE_THRESHOLD)):
                continue
            ax.scatter3D(
                xs=[-landmark.z],
                ys=[landmark.x],
                zs=[-landmark.y],
                color=self.normalize_color(landmark_drawing_spec.color[::-1]),
                linewidth=landmark_drawing_spec.thickness)
            
            frame_3d_plot["landmarks"].append([-landmark.z,landmark.x,-landmark.y])
            plotted_landmarks[idx] = (-landmark.z, landmark.x, -landmark.y)
        if connections:
            num_landmarks = len(landmark_list.landmark)
            # Draws the connections if the start and end landmarks are both visible.
            for connection in connections:
                start_idx = connection[0]
                end_idx = connection[1]
                if not (0 <= start_idx < num_landmarks and 0 <= end_idx < num_landmarks):
                    raise ValueError(f'Landmark index is out of range. Invalid connection '
                                    f'from landmark #{start_idx} to landmark #{end_idx}.')
                if start_idx in plotted_landmarks and end_idx in plotted_landmarks:
                    landmark_pair = [
                        plotted_landmarks[start_idx], plotted_landmarks[end_idx]
                    ]
                    ax.plot3D(
                        xs=[landmark_pair[0][0], landmark_pair[1][0]],
                        ys=[landmark_pair[0][1], landmark_pair[1][1]],
                        zs=[landmark_pair[0][2], landmark_pair[1][2]],
                        color=self.normalize_color(connection_drawing_spec.color[::-1]),
                        linewidth=connection_drawing_spec.thickness)
                    frame_3d_plot["connections"].append([[landmark_pair[0][0], landmark_pair[1][0]],
                                                              [landmark_pair[0][1], landmark_pair[1][1]],
                                                              [landmark_pair[0][2], landmark_pair[1][2]]])
        plt.savefig(f"sequence/karate{count}.png")
        return frame_3d_plot
        #plt.show()
    #def save_json(self):
    #    with open("karate_video")
    def findPose(self,count,img, draw=True,plot=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            if plot:
                frame_3d_plot= self.plot_landmarks(count,self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img, frame_3d_plot


    def getPosition(self, img):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def showFps(self, img):
        cTime = time.time()
        #print(cTime, self.pTime)
        fbs = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(img, str(int(fbs)), (70, 80), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

    def findAngle(self, img, p1, p2, p3, draw=True):
        # Get the landmark
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        # some time this angle comes zero, so below conditon we added
        if angle < 0:
            angle += 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 1)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 1)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 1)
            # cv2.putText(img, str(int(angle)), (x2 - 20, y2 + 50), cv2.FONT_HERSHEY_SIMPLEX,
            #             1, (0, 0, 255), 2)
        return angle


def main():
    detector = poseDetector()
    cap = cv2.VideoCapture("/home/amari/Desktop/CaesarAIFencing/videos/karate.mp4")
    length = int(cap. get(cv2. CAP_PROP_FRAME_COUNT))
    count = 0
    final_frame_json = []
    while count < length:
        success, img = cap.read()
        img,frame_3d_plot = detector.findPose(count,img,plot=True,draw=False)
        final_frame_json.append({f"frame_{count}":frame_3d_plot}) 

        lmList = detector.getPosition(img)
  
        # print(lmList)
        detector.showFps(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        count += 1

    with open("karate_frames.json","w+") as f:
        json.dump({"frames":final_frame_json},f)


if __name__ == "__main__":
    main()
