import requests
import time
import face_predict
import numpy as np
import cv2
import uuid
import mov_on_image 
from crop import crop_face_central_line


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
                "fluent": True,
                "pad_audio": 2,
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



def list_single_image_faces_info(img, bboxes):
    """
    获取单张图片的所有人脸信息
    :param img: 原图的numpy数据
    :param re_bboxes: 调整后的人脸框坐标
    
    """
    i = 0
    image2video_list =[]

    face_images_info = crop_face_central_line(img, bboxes)
    for face_image_info in face_images_info:
        # 保存裁剪后的图像
        image_file_path = f'./temp/cropped_face_{i}.jpg'
        cv2.imwrite(image_file_path, face_image_info[0]) 
        image2video_list.append([image_file_path, face_image_info[2], face_image_info[1]])
        i += 1
    return image2video_list




if __name__ == '__main__':
    did_t2v = DIDT2V()

    image_path = '/home/advance/dev/insightface/2p.png'
    bboxes, img = get_face_bboxes(image_path)
    image2video_list = list_single_image_faces_info(img, bboxes)
    for image2video in image2video_list:
        video_path = did_t2v.run(image2video[0], text_input = "请注意，这种简单的文件存储方式对于多线程或者多进程访问时可能会有并发问题，如果需要更高级的功能")
        # 将视频与图片进行合成
        mov_on_image.process_v2(image_path, video_path, image2video[1], image2video[2])

