"""
! wget https://researchmap.jp/TaisukeKawamata/avatar.jpg
! wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
"""

import os
import warnings
import numpy as np

from skimage import feature
import cv2

np.seterr(divide='ignore', invalid='ignore') # χ二乗距離で発生する0除算の警告を無視する

FACE_DETECTOR_PATH = "./haarcascade_frontalface_default.xml"
assert os.path.exists(FACE_DETECTOR_PATH), "顔検出器がありません"
FACE_DETECTOR = cv2.CascadeClassifier(FACE_DETECTOR_PATH) # 顔検出器

def Face_Detection(img:np.ndarray)->list:
    """Viola-Jonesで顔検出
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    face_rect_list = FACE_DETECTOR.detectMultiScale(img_gray)
    return face_rect_list

# https://qiita.com/tancoro/items/959ae9c14048c06bea8e
def LBPH(image, p:int=8, r:int=1, x:int=7, y:int=7, method="nri_uniform")->np.ndarray:
    bins = (p-1)*p+2+1
    if method == "default":
        bins = 2**p
    elif method == "ror" or method == "uniform":
        bins = p+3

    # 画像をLBPに変換
    lbp = feature.local_binary_pattern(
        image.reshape(image.shape[0], 
        image.shape[1]), 
        p, 
        r, 
        method=method
    )

    img_divide = [] # 画像を分割してリスト化
    [np.array(img_divide.extend(np.array_split(h_img, y, 1))) for h_img in np.array_split(lbp, x, 0)] 
    lbph = []
    for split in img_divide: # 分割領域ごとにLBPHを計算
        lbph = lbph + np.histogram(split.ravel(), bins=np.arange(bins))[0].tolist()
        
    return lbph

def Chi2(feature:np.ndarray, template:np.ndarray)->float:
    """χ二乗距離
    """
    return np.nansum((template-feature)**2/(template+feature))

def Feature_Extraction(img)->list:
    face_rect_list = Face_Detection(img) # 顔位置検出
    feature_list = []
    for x,y,w,h in face_rect_list:
        face_img = img[y:y+h, x:x+w] # 顔領域切り取り
        face_img_resize = cv2.resize(face_img, dsize=(50, 50)) # サイズ正規化
        face_img_resize_gray = cv2.cvtColor(face_img_resize, cv2.COLOR_BGR2GRAY) # グレースケール化
        feature = LBPH(face_img_resize_gray)
        feature_list.append(feature)
    return feature_list
     

def Registration(img_list:list):
    # 画像リストからテンプレート特徴量を計算
    feature_list = []
    for img in img_list:
        assert img is not None, "画像が読み込まれていません"
        feature_list_ = Feature_Extraction(img)
        feature_list.extend(feature_list_)
    if len(feature_list) > len(img_list): 
        warnings.warn("顔が複数検出された画像があります")
    if len(feature_list) < len(img_list): 
        warnings.warn("顔検出に失敗した画像があります")
    return np.mean(feature_list, axis=0)

def Examination(img, template):
    # 画像をテンプレートと照合
    assert img is not None, "画像が読み込まれていません"
    feature_list = Feature_Extraction(img) # 特徴抽出
    dist_list = []
    for feature in feature_list:
        dist = Chi2(feature, template) # 距離計算
        dist_list.append(dist)
    return np.mean(dist)

if __name__ == "__main__":
    
    # ! wget https://researchmap.jp/TaisukeKawamata/avatar.jpg
    # ! wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml

    reference_img_path = "./avatar.jpg"
    reference_img = cv2.imread("./avatar.jpg")
    reference_img_list:list = [reference_img]
    template = Registration(reference_img_list)

    verify_img_path = "./avatar.jpg"
    verify_img = cv2.imread(verify_img_path)
    distance = Examination(verify_img, template)
    print(f"距離：{distance:.2f}")