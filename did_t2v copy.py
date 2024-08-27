import requests
import time
import face_predict
import numpy as np
import cv2
import uuid
import mov_on_image 


class DIDT2V:
    def __init__(self) -> None:
        self.url = "https://api.d-id.com/talks"
        self.api_key =  "bHVveGluQGpzaGluZS5jYw:YJuT6kSXEDw6hYelNf9Sr"
        self.cloud_url = "https://beta.yxjqd.com/wxapp/aiwxapp/commons/upload"


    def upload_file(self, file_path):
        response = requests.post(url=self.cloud_url, files={"file": open(file_path, "rb")})
        # print(response.text)
        if response.json()["msg"] == '上传成功':
            print("upload file success")
            return response.json()["data"]
        else: 
            raise Exception("upload file failed")


    def send_task(self, image_url, text_input=""):
        # print("==============", text_input)
        if text_input == "":
            text_input = "首先，作为广告主，您入驻平台后可以享受免佣金的内容派单发布服务，这将帮助您节约市场推广费用。"
        print("==============", text_input)
        payload = {
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "zh-CN-XiaoyiNeural"
                },
                "input": text_input

            },
            "config": {
                "fluent": "false",
                "pad_audio": "0.0",
                "stitch": True
       
            },
            "source_url": image_url

        }

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Basic {self.api_key}"
                                
        }

        response = requests.post(self.url, json=payload, headers=headers)
        print(response.text)
        if response.json()["status"] == "created":
            task_id = response.json()["id"]
            print(f"task_id=======>:{task_id}")
            return task_id
        else:
            raise Exception("video creation failed")


    def get_history(self, task_id="")->str:
        """
        Get the result of the task by task_id.

        :param task_id: task id
        :return: result url
        """

        url = f"https://api.d-id.com/talks/{task_id}"

        headers = {"accept": "application/json",
                "authorization": f"Basic {self.api_key}"}

        for turn in range(10):
            time.sleep(2)
            response = requests.get(url, headers=headers)
            # print(response.text)
            print(response.json())
            if response.json().get("result_url"):
                break

        return response.json().get("result_url")    


        # else:
        #     raise Exception("get history failed")

    def run(self, image_file_path, text_input = "请问如何解决推广费？"):
        # 上传图片
        image_url = self.upload_file(image_file_path)
        # 制作视频
        task_id = self.send_task(image_url, text_input)
        result_url = self.get_history(task_id=task_id)

        # 获取视频并保存在本地
        video = requests.get(result_url)
        video = video.content
        video_path = "./temp/" + str(uuid.uuid4()) + ".mp4"
        # 保存在本地
        with open(video_path, "wb") as f:
            f.write(video)
        return video_path



def get_face_bboxes(img):
    """
    获取人脸框的坐标
    :param img: 图片的路径
    :return: 人脸框的坐标, 原图的numpy数据格式
    """
    bboxes = []
    faces, img = face_predict.predict(img)
    for face in faces:
        bboxes.append(face["bbox"])
    return bboxes, img


# 重新调整框的坐标
def readjustment_bbox(bboxes, img, scale = 0.6):
    """
    调整框的坐标

    :param bboxes: 人脸框的坐标
    :param img: 原图的numpy数据
    :param scale: 缩放比例
    :return: 调整后的坐标
    """

    re_bboxes = []
    for bbox in bboxes:
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]  
        # 对框的大小按照比例进行缩放
        
        # 框的中心点（x0,y0）    
        x0 = (bbox[0]+bbox[2])/2
        y0 = (bbox[1]+bbox[3])/2

        x1 = x0-(w/2)*(1+scale)
        y1 = y0-(h/2)*(1+scale)
        x2 = x0+(w/2)*(1+scale) 
        y2 = y0+(h/2)*(1+scale)

        # 判断是否越界
        if x1<0:
            x1 = 0
        if y1<0:
            y1 = 0

        if x2>img.shape[1]:
            x2 = img.shape[1]
        if y2>img.shape[0]:
            y2 = img.shape[0]
        re_bboxes.append([x1, y1, x2, y2])

    return re_bboxes

# 根据中心线进行裁剪
def crop_face_central_line(img, bboxes):
    """
    对人脸框进行裁剪，以中心线为中心进行裁剪
    :param img: 原图的numpy数据
    :param bboxes: 人脸框的坐标
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = (int(i) for i in bbox)

    # 计算两个框的之间的中心线
    center_line_x = int((x1+x2)/2)
    face_image_left = img[:, :center_line_x]
    face_image_right = img[:, center_line_x:]

    return face_image_left, face_image_right





# 正方形框
# 根据对角坐标对人脸进行裁剪
def crop_face(img, bbox):
    """
    Crop face from image given bounding box
    :param img: 原图的numpy数据
    :param bbox: 人脸框的坐标

    :return: 
    face_image: 裁剪后的人脸图像
    size: 裁剪后的人脸框大小
    center: 裁剪后的人脸框中心点
    mark: 裁剪的方式标记
    """
    x1, y1, x2, y2 = (int(i) for i in bbox)
    w = x2 - x1
    h = y2 - y1

    # 将框的形状调整为正方形
    if w%2!=0:
        x2 = x2-1
    if h%2!=0:
        y2 = y2-1
    # 计算框的中心点
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    center = (x0, y0)
    # 重新计算宽高
    w = x2 - x1
    h = y2 - y1
    if w>h:
        size = (w, w)
    else:
        size = (h, h)

    # 计算正方形框的左上角和右下角坐标
    # 左上角
    x1 = int(center[0] - size[0] / 2)
    y1 = int(center[1] - size[1] / 2)
    # 右下角
    x2 = int(center[0] + size[0] / 2)
    y2 = int(center[1] + size[1] / 2)
    # 判断是否越界
    if x1<0:
        x1 = 0
    if y1<0:
        y1 = 0

    if x2>img.shape[1]:
        x2 = img.shape[1]
    if y2>img.shape[0]:
        y2 = img.shape[0]
        
    # 重新计算框的中心点
    x0 = (x1 + x2) / 2
    y0 = (y1 + y2) / 2
    center = (x0, y0)

    if y1<=0 or y2>=img.shape[0] or x1<=0 or x2>=img.shape[1]:
        mark = None
        # 创建一个全黑的图像
        face_image = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        # 左边的框
        # 左上角
        if y1<=0:
            if w>h:
                face_image[w-h:, :, :] = img[y1:y2, x1:x2, :]
                # NOTE did那边做完之后按照这个格式：face_image[w-h:, :, :]，进行剪裁
                mark = 1
        
        if x1<=0:
            if h>w:
                face_image[:, h-w:, :] = img[y1:y2, x1:x2, :]
                mark = 2
        # 左下角
        if y2>=img.shape[0]:
            if w>h:
                face_image[:h, :, :] = img[y1:y2, x1:x2, :]
                mark = 3
        if x1<=0:
            if h>w:
                face_image[:, :w, :] = img[y1:y2, x1:x2, :]
                mark = 4

        # 右边的框
        # 右上角
        if y1<=0:
            if w>h:
                face_image[w-h:, :, :] = img[y1:y2, x1:x2, :]
                mark = 5
        if x2>=img.shape[1]:
            if h>w:
                face_image[:, :w, :] = img[y1:y2, x1:x2, :]
                mark = 6
        # 右下角
        if y2>=img.shape[0]:
            if w>h:
                face_image[:h, :, :] = img[y1:y2, x1:x2, :]
                mark = 7
        if x2>=img.shape[1]:
            if h>w:
                face_image[:, :w, :] = img[y1:y2, x1:x2, :]
                mark = 8
    else:
        face_image = img[y1:y2, x1:x2]
        mark = 0
    
    return face_image, size, center, mark



def list_single_image_faces_info(img, re_bboxes):
    """
    获取单张图片的所有人脸信息
    :param img: 原图的numpy数据
    :param re_bboxes: 调整后的人脸框坐标
    
    """
    i = 0
    image2video_list =[]
    for re_bbox in re_bboxes:
        
        face_image, size, center, mark = crop_face(img, re_bbox)
        # 保存裁剪后的图像
        image_file_path = f'./temp/cropped_face_{i}.jpg'
        cv2.imwrite(image_file_path, face_image) 
        image2video_list.append([image_file_path, size, center, mark])
        i += 1
        print(face_image.shape, size, center, mark)
    return image2video_list





if __name__ == '__main__':
    did_t2v = DIDT2V()

    image_path = '/home/advance/dev/insightface/2p.png'
    bboxes, img = get_face_bboxes(image_path)
    re_bboxes = readjustment_bbox(bboxes, img)
    image2video_list = list_single_image_faces_info(img, re_bboxes)
    for image2video in image2video_list:
        video_path = did_t2v.run(image2video[0], text_input = "请注意，这种简单的文件存储方式对于多线程或者多进程访问时可能会有并发问题，如果需要更高级的功能")
        # 将视频与图片进行合成
        mov_on_image.process(image_path, video_path, image2video[1], image2video[2])

