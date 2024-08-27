#coding=utf-8

'''
requires Python 3.6 or later
pip install requests
'''
import json
import uuid
import requests
from .common import load_yaml_config
import os
import base64


class T2A:
    def __init__(self):
        self.dirname = os.path.dirname(os.path.abspath(__file__))
        self.config = load_yaml_config(self.dirname+"/config.yaml")["Doubao"]
        print(self.config)
        self.appid = self.config["appid"]
        self.access_token = self.config["access_token"]
        self.cluster = self.config["cluster"]
        self.voice_type = self.config["voice_type"]
        self.host = self.config["host"]
        self.api_url = f"https://{self.host}/api/v1/tts"
        self.header = {"Authorization": f"Bearer;{self.access_token}"}


    def get_payload(self, text, voice_type="BV115_streaming"):
        request_json = {
            "app": {
                "appid": self.appid,
                "token": "access_token",
                "cluster": self.cluster
            },
            "user": {
                "uid": "388808087185088"
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": "mp3",
                "speed_ratio": 1.0,
                "volume_ratio": 1.0,
                "pitch_ratio": 1.0,
            },
            "request": {
                "reqid": str(uuid.uuid4()),
                "text": text,
                "text_type": "plain",
                "operation": "query",
                "with_frontend": 1,
                "frontend_type": "unitTson"

            }
        }

        return json.dumps(request_json)

    
    def convert(self, text, voice_type):
        request_json = self.get_payload(text, voice_type)
        try:
            resp = requests.post(self.api_url, data=request_json, headers=self.header)
            # print(resp.content)
            if "data" in resp.json():
                base64_audio = resp.json()["data"]
                audio_path = os.path.dirname(self.dirname)+ f"/temp/audio_{uuid.uuid4()}.mp3"
                print("音频文件临时保存路径====>", audio_path)
                with open(audio_path, "wb") as f:
                    f.write(base64.b64decode(base64_audio))
                return base64_audio, audio_path
        except Exception as e:
            print(e)
        


