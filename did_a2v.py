import requests
import time
import face_predict
import cv2
import uuid
import mov_on_image 
from crop import crop_face_central_line


class DIDT2V:
    def __init__(self) -> None:
        self.url = "https://api.d-id.com/talks"
        self.api_key =  "bHVveGluQGpzaGluZS5jYw:YJuT6kSXEDw6hYelNf9Sr"
        self.cloud_url_image = "https://beta.yxjqd.com/wxapp/aiwxapp/commons/upload"
        self.cloud_url_audio = "https://beta.yxjqd.com/wxapp/aiwxapp/commons/file/upload"

    def upload_file(self, file_path)->str:
        """
        返回一个图片的url
        """

        # 获取文件名前缀
        suffix = file_path.split("/")[-1].split(".")[-1]

        if suffix in ["jpg", "png", "jpeg"]:
            response = requests.post(url=self.cloud_url_image, files={"file": open(file_path, "rb")})
            # print(response.text)
            if response.json()["msg"] == '上传成功':
                print("upload image file success")
                return response.json()["data"]
            else: 
                raise Exception("upload image file failed")

        else:
            response = requests.post(url=self.cloud_url_audio, data={"type":2}, files={"file": open(file_path, "rb")} )
            if response.json()["msg"] == '上传成功':
                print("upload audio file success")
                return response.json()["data"]
            else: 
                raise Exception("upload audio file failed")



    def send_task(self, image_url:str, audio_url:str=""):
        print("image_url===>",image_url)
        print("audio_url===>",audio_url)
        payload = {
            "script": {
                "type": "audio",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "zh-CN-XiaoyiNeural"
                },
                "audio_url": audio_url,
                "reduce_noise": True

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


    def run(self, image_file_path, audio_file_path):
        # 上传图片
        image_url = self.upload_file(image_file_path)
        audio_url = self.upload_file(audio_file_path)
        # 制作视频
        task_id = self.send_task(image_url, audio_url)
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






