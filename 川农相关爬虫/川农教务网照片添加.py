import requests
import json
import base64
import glob
import os
import shutil

class Faceset():
    # 此函数用于获取access_token，返回access_token的值
    # 此函数被parse_face_pic调用

    def get_access_token(self):
        client_id = 'G9yWRpQRxqGLl0vZv2MIqoNE'                # 此变量赋值成自己API Key的值
        client_secret = 'RLol5YGP3EUIEgmQskKLScYvUm3cySvx'    # 此变量赋值成自己Secret Key的值
        auth_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret

        response_at = requests.get(auth_url)
        json_result = json.loads(response_at.text)
        access_token = json_result['access_token']
        return access_token

    # 此函数进行人脸识别，返回识别到的人脸列表
    # 此函数被parse_face_pic调用

    def identify_faces(self, url_pic, url_fi):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        f = open(url_pic, 'rb')
        # 参数image：图像base64编码 以及face_fields参数
        # image的值取决于 image_type
        img = base64.b64encode(f.read())
        post_data = {
            'user_id': url_pic[-13:-4],
            'uid': url_pic[-13:-4],
            'group_id': url_pic[-13:-9],
            'image': str(img, 'utf-8'),
            'image_type': 'BASE64',
            'user_info': url_pic[-13:-4]
        }

        response_fi = requests.post(url_fi, headers=headers, data=post_data)
        json_fi_result = json.loads(response_fi.text)
        return json_fi_result
        # 此函数调用get_access_token、identify_faces

    def parse_face_pic(self, url_pic):
        # 调用get_access_token获取access_token
        access_token = self.get_access_token()
        url_fi = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token=' + access_token
        # 调用identify_faces，
        l = glob.glob(url_pic + '*.jpg')
        num = 0
        for i in l:
            num += 1
            try:
                json_faces = self.identify_faces(i, url_fi)
                print(num, i[-13:-4], json_faces['error_msg'], json_faces['log_id'])
            except:
                print(i)

if __name__ == '__main__':
    # l ='/home/duansq/duan/test/'
    l = input('Please input path you want to analysis:')
    bfi = Faceset()
    bfi.parse_face_pic(l)
