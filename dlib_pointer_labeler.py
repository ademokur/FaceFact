import dlib
import cv2 as cv2
import os
import imutils
import numpy as np

from imutils import face_utils
from scipy.spatial import distance as dist

class dlib_pointer:
    def __init__(self,shape_predictor_path = "shape_predictor_68_face_landmarks.dat"):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(shape_predictor_path)

    def euclidean_finder(self,a,b):
        A = dist.euclidean(a, b)

        return A

    def x_y_lister2(self,x_y_list):
        lst = []
        mouth_l = []
        right_eyebrow_l = []
        left_eyebrow_l = []
        right_eye_l = []
        left_eye_l = []
        nose_l = []
        jaw_l = []
        indexs = []
        bfr = None
        for (index, (name, (x, y))) in x_y_list:
            if bfr == None:
                bfr = index

            if bfr != index:
                bfr = index
                indexs.append(mouth_l)
                indexs.append(right_eyebrow_l)
                indexs.append(left_eyebrow_l)
                indexs.append(right_eye_l)
                indexs.append(left_eye_l)
                indexs.append(nose_l)
                indexs.append(jaw_l)
                lst.append(indexs)

                mouth_l = []
                right_eyebrow_l = []
                left_eyebrow_l = []
                right_eye_l = []
                left_eye_l = []
                nose_l = []
                jaw_l = []
                indexs = []

            if name == "mouth":
                mouth_l.append((index, (x, y)))
            if name == "right_eyebrow":
                right_eyebrow_l.append((index, (x, y)))
            if name == "left_eyebrow":
                left_eyebrow_l.append((index, (x, y)))
            if name == "right_eye":
                right_eye_l.append((index, (x, y)))
            if name == "left_eye":
                left_eye_l.append((index, (x, y)))
            if name == "nose":
                nose_l.append((index, (x, y)))
            if name == "jaw":
                jaw_l.append((index, (x, y)))


        indexs.append(mouth_l)
        indexs.append(right_eyebrow_l)
        indexs.append(left_eyebrow_l)
        indexs.append(right_eye_l)
        indexs.append(left_eye_l)
        indexs.append(nose_l)
        indexs.append(jaw_l)
        lst.append(indexs)

        return lst

    def set_image(self,path,width = None):
        self.image_path = path
        try:
            self.image = cv2.imread(path)
            if width != None:
                self.image = imutils.resize(self.image,width=width)
        except:
            self.image = path
            self.image_path = None

    def resize_img(self,x,y):
        print("[WARNING] Resizing might affect process badly!")
        self.image = cv2.resize(self.image,(x,y))

    def change_image_type(self,type_of_cv2 = cv2.COLOR_BGR2GRAY):
        self.image = cv2.cvtColor(self.image,type_of_cv2)
        print(f"[INFO] Image converted to '{type_of_cv2}'")

    def mark_points(self,draw_on_img = True):
        roi_list = []
        shape_list = []
        x_y_list = []

        rects = self.detector(self.image, 1)

        roi = []
        shape = []
        x_y = []
        for (index, rect) in enumerate(rects):
            shape = self.predictor(self.image, rect)
            shape = face_utils.shape_to_np(shape)
            shape_list.append((index,shape))

            for (name, (index1,j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
                for (x, y) in shape[index1:j]:
                    x_y_list.append((index,(name,(x,y))))
                    if draw_on_img:
                        cv2.circle(self.image, (x, y), 1, (0, 0, 255), -1)

                    (x, y, w, h) = cv2.boundingRect(
                        np.array([shape[index1:j]]))
                    roi = self.image[y:y + h, x:x + w]
                roi_list.append((index,(name,roi)))

        if len(roi_list) == 0:
            roi_list.append(roi)

        if len(shape_list) == 0:
            shape_list.append(shape)

        if len(x_y_list) == 0:
            x_y_list.append(x_y)

        return roi_list,shape_list,x_y_list

    def draw_circles_on_board(self,x_y_list,radius=1,color=(0,0,255),thickness=-1,do_not_draw=[],make_it_gray=False,board = None):
        # for 'do_not_draw' = ["mouth","nose","jaw","left_eye","right_eye","left_eyebrow","right_eyebrow"]
        try:
            if board == None:
                board = np.ones_like(self.image)
        except:
            pass

        for (index, (name, (x, y))) in x_y_list:
            if not do_not_draw.count(name):
                cv2.circle(board, (x, y),radius, color, thickness)

        if make_it_gray:
            board = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
            print("[INFO] Board converted to gray.")

        return board

    def connect_circles(self,x_y_list,board = None,color=(0,0,255),thickness=1,do_not_draw=[],make_it_gray=False,do_not_connect_lasts=["jaw","left_eyebrow","right_eyebrow","mouth"],special_mouth = True):
        # for 'do_not_draw' = ["mouth","nose","jaw","left_eye","right_eye","left_eyebrow","right_eyebrow"]
        draw_list = ["mouth", "nose", "jaw", "left_eye", "right_eye", "left_eyebrow", "right_eyebrow"]
        try:
            if board == None:
                board = np.ones_like(self.image)
        except:
            pass

        for obj in draw_list:
            if not do_not_draw.count(obj):
                bfr = None
                first_xy = None
                bfr_index = None
                twelfe = None
                for i,(index, (name, (x, y))) in enumerate(x_y_list):
                    if bfr_index == None:
                        bfr_index = index

                    if bfr_index != index:
                        bfr_index = index
                        bfr = None
                        first_xy = None

                    if name == obj:
                        if first_xy == None:
                            first_xy = (x,y)

                        if bfr == None:
                            bfr = (x,y)

                        if name == "mouth" and special_mouth == True:
                            if i == 11:
                                cv2.line(board, first_xy, (x, y), color, thickness)

                            if i == 12:
                                bfr = (x, y)
                                twelfe = (x,y)

                            if i == 19:
                                cv2.line(board, twelfe, (x, y), color, thickness)

                            cv2.line(board, bfr, (x, y), color, thickness)
                            bfr = (x, y)

                        else:
                            cv2.line(board,bfr,(x,y),color,thickness)
                            bfr = (x,y)

                if not do_not_connect_lasts.count(obj):
                        cv2.line(board, bfr, first_xy, color, thickness)

        if make_it_gray:
            board = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
            print("[INFO] Board converted to gray.")

        return board

    def special_connector(self,x_y_list,board = None,color=(0,0,255),thickness=1,radius = 3,do_not_draw=[],make_it_gray=False,draw_points = True):
        # for 'do_not_draw' = ["mouth","nose","jaw","left_eye","right_eye","left_eyebrow","right_eyebrow"]
        draw_list = ["mouth", "nose", "jaw", "left_eye", "right_eye", "left_eyebrow", "right_eyebrow"]
        try:
            if board == None:
                board = np.ones_like(self.image)
        except:
            pass

        x_y_list2 = self.x_y_lister2(x_y_list)

        for obj in draw_list:#mouth right_eyebrow left_eyebrow right_eye left_eye nose jaw
            if not do_not_draw.count(obj):
                q = 0
                bf_n = None
                jw_left = 13
                for (index, (name, (x, y))) in x_y_list:
                    if bf_n == None:
                        bf_n = name

                    if bf_n != name:
                        bf_n = name
                        q = 0

                    try:
                        if name == "left_eye" and q == 0:
                            cv2.line(board, (x,y), x_y_list2[int(index)][4][3][1], (255,0,150), thickness)#gözün sonu
                            cv2.line(board, (x, y), x_y_list2[int(index)][2][2][1], (255,0,150), thickness)#kaşın ortası
                            cv2.line(board, (x, y), x_y_list2[int(index)][3][3][1], (255,0,150), thickness)#diğer gözün sonu
                            cv2.line(board, (x, y), x_y_list2[int(index)][5][6][1], (30, 0, 150),thickness)#burnun ortası
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "left_eye" and q == 3:
                            cv2.line(board, (x,y), x_y_list2[int(index)][6][jw_left][1], (255,0,150), thickness)#jaw ile, might be 11 or 13
                            cv2.line(board, (x,y), x_y_list2[int(index)][5][8][1], (255,0,150), thickness)#burunun kenarı ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "left_eyebrow" and q == 2:
                            cv2.line(board, (x,y), x_y_list2[int(index)][1][2][1], (255,0,150), thickness)#kaşların birleşimi
                            cv2.line(board, (x,y), x_y_list2[int(index)][4][3][1], (255,0,150), thickness)#kaşın göz sonu ile birleşimi
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "right_eye" and q == 0:
                            cv2.line(board, (x,y), x_y_list2[int(index)][3][3][1], (255,0,150), thickness)#gözün sonu
                            cv2.line(board, (x, y), x_y_list2[int(index)][1][2][1], (255,0,150), thickness)#kaşın ortası
                            cv2.line(board, (x, y), x_y_list2[int(index)][6][4][1], (255,0,150), thickness)#jaw ile
                            cv2.line(board, (x, y), x_y_list2[int(index)][5][4][1], (255, 0, 150),thickness)#burunun kenarı ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "right_eye" and q == 3:
                            cv2.line(board, (x, y), x_y_list2[int(index)][5][6][1], (30, 0, 150),thickness)#burnun ortası
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "right_eyebrow" and q == 2:
                            cv2.line(board, (x, y), x_y_list2[int(index)][3][3][1], (255, 0, 150),thickness)#gözün sonu
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "nose" and q == 6:
                            cv2.line(board, (x, y), x_y_list2[int(index)][5][8][1], (30, 0, 150), thickness)#burunun kenarı ile
                            cv2.line(board, (x, y), x_y_list2[int(index)][5][4][1], (30, 0, 150), thickness)#burunun kenarı ile
                            cv2.line(board, (x, y), x_y_list2[int(index)][0][0][1], (30, 0, 150), thickness)#dudağın kenarı ile
                            cv2.line(board, (x, y), x_y_list2[int(index)][0][6][1], (30, 0, 150), thickness)#dudağın kenarı ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)
                                cv2.circle(board, x_y_list2[int(index)][5][8][1], radius, color, thickness)
                                cv2.circle(board, x_y_list2[int(index)][5][4][1], radius, color, thickness)

                        if name == "nose" and q == 4:
                            cv2.line(board, (x, y), x_y_list2[int(index)][0][0][1], (255, 0, 150), thickness)#burunun kenarı ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "nose" and q == 8:
                            cv2.line(board, (x, y), x_y_list2[int(index)][0][6][1], (255, 0, 150), thickness)#burunun kenarı ile
                            if draw_points:
                                cv2.ircle(board, (x, y), radius, color, thickness)

                        if name == "mouth" and q == 0:
                            cv2.line(board, (x, y), x_y_list2[int(index)][6][4][1], (255, 0, 150), thickness)#jaw ile
                            cv2.line(board, (x, y), x_y_list2[int(index)][6][8][1], (255, 0, 150), thickness)#jawın ortası ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "mouth" and q == 6:
                            cv2.line(board, (x, y), x_y_list2[int(index)][6][jw_left][1], (255, 0, 150),thickness)#jaw ile
                            cv2.line(board, (x, y), x_y_list2[int(index)][6][8][1], (255, 0, 150),thickness)#jawın ortası ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)

                        if name == "jaw" and (q == 4 or q == jw_left):
                            cv2.line(board, (x, y), x_y_list2[int(index)][6][8][1], (255, 0, 150),thickness)  # jawın ortası ile
                            if draw_points:
                                cv2.circle(board, (x, y), radius, color, thickness)
                                cv2.circle(board, x_y_list2[int(index)][6][8][1], radius, color, thickness)

                    except:
                        pass

                    q += 1

        if make_it_gray:
            board = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
            print("[INFO] Board converted to gray.")

        return board

    def find_eyes_center(self,x_y_list,board = None,color=(255,0,0),thickness=1,make_it_gray=False,draw_on_it = True):
        # for 'do_not_draw' = ["mouth","nose","jaw","left_eye","right_eye","left_eyebrow","right_eyebrow"]
        try:
            if board == None:
                board = np.ones_like(self.image)
        except:
            pass

        left_eye_l = []
        right_eye_l = []
        for (index, (name, (x, y))) in x_y_list:
            if name == "left_eye" :
                left_eye_l.append((x,y))

            if name == "right_eye":
                right_eye_l.append((x,y))

        mean_x_left_eye = (left_eye_l[0][0] + left_eye_l[3][0])/2

        mean_y1_left_eye = (left_eye_l[1][1] + left_eye_l[2][1])/2
        mean_y2_left_eye = (left_eye_l[4][1] + left_eye_l[5][1])/2

        mean_y_left_eye = (mean_y1_left_eye+mean_y2_left_eye)/2
        if draw_on_it:
            cv2.circle(board, (int(mean_x_left_eye), int(mean_y_left_eye)), 1, color, thickness)
        left_mean = (int(mean_x_left_eye), int(mean_y_left_eye))

        mean_x_right_eye = (right_eye_l[0][0] + right_eye_l[3][0])/2

        mean_y1_right_eye = (right_eye_l[1][1] + right_eye_l[2][1])/2
        mean_y2_right_eye = (right_eye_l[4][1] + right_eye_l[5][1])/2

        mean_y_right_eye = (mean_y1_right_eye+mean_y2_right_eye)/2
        if draw_on_it:
            cv2.circle(board, (int(mean_x_right_eye), int(mean_y_right_eye)), 1, color, thickness)
        right_mean = (int(mean_x_right_eye), int(mean_y_right_eye))


        if make_it_gray:
            board = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
            print("[INFO] Board converted to gray.")

        return board,(right_mean,left_mean)

    def show_image(self,wname = "image",wk = 0,justret = False):
        if justret:
            return self.image
        if not justret:
            cv2.imshow(wname,self.image)
            cv2.waitKey(wk)
            cv2.destroyWindow(wname)

        return self.image

    def find_open_mouth(self,x_y_list,on_board = None,hold = 1):
        lst = self.x_y_lister2(x_y_list)

        mouths = []

        for ind in lst:
            euc = self.euclidean_finder(ind[0][14][1],ind[0][18][1])
            euc2 = self.euclidean_finder(ind[0][3][1],ind[0][4][1])

            rate = round(euc2/euc,3)
            smile = False
            if rate <= hold:
                smile = True

            try:
                if on_board != None:
                    cv2.putText(on_board, str(smile), (ind[0][0][1][0], ind[0][14][1][1]),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)
            except:
                cv2.putText(on_board, str(smile), (ind[0][0][1][0],ind[0][14][1][1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)

                mouths.append([smile,rate])

        return mouths

    def find_open_eye(self,x_y_list,on_board = None,hold = 1.75):
        lst = self.x_y_lister2(x_y_list)

        eyes = []

        for ind in lst:
            open = True
            euc = self.euclidean_finder(ind[3][1][1],ind[3][5][1])
            euc2 = self.euclidean_finder(ind[3][1][1],ind[3][2][1])

            rate = round(euc2/euc,3)
            if rate > hold:
                open = False

            euc = self.euclidean_finder(ind[4][1][1],ind[4][5][1])
            euc2 = self.euclidean_finder(ind[4][1][1],ind[4][2][1])

            rate = round(euc2/euc,3)

            if rate > hold:
                open = False

            eyes.append([open,rate])
            try:
                if on_board != None:
                    cv2.putText(on_board, str(open), (ind[3][0][1][0], ind[3][6][1][1]),cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)
            except:
                cv2.putText(on_board, str(open), (ind[3][0][1][0],ind[3][0][1][1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1)

        return eyes

    def find_smile(self,x_y_list,hold = 7.5):
        lst = self.x_y_lister2(x_y_list)

        smiles = []

        for ind in lst:
            # cv2.circle(board, ind[5][4][1], 3, (255,0,255), 2)
            # cv2.circle(board, ind[0][0][1], 3, (255,0,255), 2)

            euc = self.euclidean_finder(ind[5][4][1],ind[0][0][1])
            euc2 = self.euclidean_finder(ind[5][8][1], ind[0][6][1])
            euc3 = self.euclidean_finder(ind[0][0][1], ind[0][6][1])

            son = False
            diff = round(euc+euc2,2) - round(euc3,2)
            if diff <= hold:
                son = True

            smiles.append([son,diff])

        return smiles

    def evaluate(self,mouths,eyes_o,smiles):
        last = ""
        for i,(mouth,eye,smile) in enumerate(zip(mouths,eyes_o,smiles)):
            moutht = "close"
            if mouth[0]:
                moutht = "open"

            eyet = "close"
            if eye[0]:
                eyet = "open"

            smilet = False
            if smile[0]:
                smilet = True

            last += f"In {i}. face, mouth is {moutht}, eye is {eyet}, is human smile = {smilet} -- "

        last = last.strip()
        last = last.strip(" --")

        return last

    def make_it_straight(self,x_y_list,board = None,face_fhandle = 0,set_as_image = True):
        try:
            if board == None:
                board = np.ones_like(self.image)
        except Exception as e:
            print(e)
            pass

        eyes = []
        lst = self.x_y_lister2(x_y_list)

        for i,ind in enumerate(lst):
            if i == face_fhandle:
                euc = (ind[3][3][1][1]-ind[4][0][1][1])

                rows, cols, _ = self.image.shape
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 360-int(euc), 1)
                converted_image = cv2.warpAffine(self.image, M, (cols, rows))

        if set_as_image:
            self.image = converted_image

        return converted_image

if __name__ == '__main__':
    PATH = "images"
    pointer = dlib_pointer()

    def on_path(PATH):
        for img in os.listdir(PATH):
            if img.endswith(".jpg") or img.endswith(".png") or img.endswith("jpeg"):
                path_img = os.path.join(PATH,img)
                pointer.set_image(path_img,width=500)

                roi_list, shape_list, x_y_list = pointer.mark_points(draw_on_img=False)

                if len(x_y_list) != 1:
                    pointer.make_it_straight(x_y_list)
                    roi_list, shape_list, x_y_list = pointer.mark_points(draw_on_img=False)
                    if len(x_y_list) != 1:

                        board = pointer.draw_circles_on_board(x_y_list, color=(0, 0, 255), radius=2)
                        board = pointer.connect_circles(x_y_list, color=(255, 255, 255), board=board, special_mouth=True,do_not_connect_lasts=["jaw", "nose", "mouth","left_eyebrow","right_eyebrow"])
                        board, (right_mean, left_mean) = pointer.find_eyes_center(x_y_list, color=(255, 255, 255), board=board)
                        board2 = pointer.special_connector(x_y_list, color=(255, 255, 255),board=pointer.show_image(justret=True).copy())
                        mouths = pointer.find_open_mouth(x_y_list,board,hold=1)
                        eyes_o = pointer.find_open_eye(x_y_list,board,hold=1.75)
                        smiles = pointer.find_smile(x_y_list,hold=5)
                        evaluate_of_face = pointer.evaluate(mouths, eyes_o,smiles)
                        print(evaluate_of_face)
                        img = pointer.show_image(justret=True)

                        cv2.imshow("board",board)
                        cv2.imshow("board2",board2)
                        cv2.imshow("img",img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()

    def on_cam(cam_n = 0,flip = True):

        cap = cv2.VideoCapture(cam_n)
        while True:
            _,frame = cap.read()

            if flip:
                frame = cv2.flip(frame,1)

            pointer.set_image(frame)

            roi_list, shape_list, x_y_list = pointer.mark_points(draw_on_img=False)

            if len(x_y_list) != 1:
                pointer.make_it_straight(x_y_list)
                roi_list, shape_list, x_y_list = pointer.mark_points(draw_on_img=False)
                if len(x_y_list) != 1:

                    board = pointer.draw_circles_on_board(x_y_list,color=(0,0,255),radius=2)
                    board = pointer.connect_circles(x_y_list, color=(255, 255, 255), board=board, special_mouth=True,do_not_connect_lasts=["jaw", "nose", "mouth","left_eyebrow","right_eyebrow"])
                    board,(right_mean,left_mean) = pointer.find_eyes_center(x_y_list, color=(255, 255, 255),board=board)
                    board2 = pointer.special_connector(x_y_list, color=(255, 255, 255), board=pointer.show_image(justret=True).copy())
                    mouths = pointer.find_open_mouth(x_y_list,on_board = board,hold=2.75)
                    eyes_o = pointer.find_open_eye(x_y_list, board,hold=1.25)
                    smiles = pointer.find_smile(x_y_list, hold=5)
                    evaluate_of_face = pointer.evaluate(mouths, eyes_o,smiles)
                    print(evaluate_of_face)

                    cv2.imshow("board",board)
                    cv2.imshow("board2",board2)

            cv2.imshow("frame",frame)

            key = cv2.waitKey(10)

            if key == 27:
                cap.release()
                cv2.destroyAllWindows()
                break

    on_path(PATH)
    # on_cam()
