import requests
import json
import base64
import glob
import os
import shutil

class BaiduFaceIdentify():
    # 此函数用于创建文件夹，此函数被parse_face_pic调用
    def creat_folder(self, path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
            print("--- Created %s ---" % path)
        else:
            print("--- Exists %s ---" % path)

    # 此函数用于获取access_token，返回access_token的值
    # 此函数被parse_face_pic调用

    def get_access_token(self):
        client_id = 'G9yWRpQRxqGLl0vZv2MIqoNE'                # 此变量赋值成自己API Key的值
        client_secret = 'RLol5YGP3EUIEgmQskKLScYvUm3cySvx'    # 此变量赋值成自己Secret Key的值
        auth_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret

        response_at = requests.get(auth_url, timeout=2)
        json_result = json.loads(response_at.text)
        access_token = json_result['access_token']
        return access_token

    # 此函数进行人脸识别，返回识别到的人脸列表
    # 此函数被parse_face_pic调用

    def identify_faces(self, url_pic, url_fi):
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        f = open(url_pic, 'rb')
        # 参数image：图像base64编码 以及face_fields参数
        # image的值取决于 image_type
        img = base64.b64encode(f.read())
        post_data = {
            'image': str(img, 'utf-8'),
            'image_type': 'BASE64',
            'face_field': 'gender,age,beauty,glasses,expression,race,faceshape',#landmark,quality,
            'max_face_num': 2
        }

        response_fi = requests.post(url_fi, headers=headers, data=post_data, timeout=2)
        json_fi_result = json.loads(response_fi.text)
        return json_fi_result['result']['face_list']
        # 下边的print也许是最直观，你最想获取人脸列表要的
        # print(json_fi_result['result']['face_list'][0]['age'])
        # print(json_fi_result['result']['face_list'][0]['beauty'])
        # 此函数用于解析进行人脸图片，输出图片上的人脸的性别、年龄、颜值
        # 此函数调用get_access_token、identify_faces

    def add_user(self, url_pic, url_fi, user_info):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        f = open(url_pic, 'rb')
        # 参数image：图像base64编码 以及face_fields参数
        # image的值取决于 image_type
        img = base64.b64encode(f.read())
        post_data = {
            'user_id': url_pic[-12:-4],
            'uid': url_pic[-12:-4],
            'group_id': url_pic[-12:-8],
            'image': str(img, 'utf-8'),
            'image_type': 'BASE64',
            'user_info': user_info,
            'action_type': 'replace'
        }

        response_fi = requests.post(url_fi, headers=headers, data=post_data, timeout=2)
        json_fi_result = json.loads(response_fi.text)
        return json_fi_result

    def parse_face_pic(self, url_pic):
        # 调用get_access_token获取access_token
        access_token = self.get_access_token()
        url_fi = 'https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token=' + access_token
        url_add_user = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add?access_token=' + access_token
        # 调用identify_faces，
        l = glob.glob(url_pic + '*.jpg')
        txt_fi = url_pic + 'out.txt'
        txt = open(txt_fi, 'a+')
        NaN = url_pic + 'NaN'
        Normal_Male = url_pic + 'Normal_Male'
        Normal_Female = url_pic + 'Normal_Female'
        Good_Male = url_pic + 'Good_Male'
        Good_Female = url_pic + 'Good_Female'
        self.creat_folder(NaN)
        self.creat_folder(Normal_Male)
        self.creat_folder(Normal_Female)
        self.creat_folder(Good_Male)
        self.creat_folder(Good_Female)
        num = 0
        for i in l:
            num += 1
            try:
                json_faces = self.identify_faces(i, url_fi)
                json_face = json_faces[0]
                b = str(json_face['gender']['type']) + ' ' + str(json_face['beauty']) + ' ' + str(json_face['face_shape']['type']) + ' ' + str(json_face['glasses']['type']) +' ' + str(json_face['race']['type'])
                add_user = self.add_user(i, url_add_user, b)
                if json_face['gender']['type'] == 'male':
                    if json_face['beauty'] >= 60:
                        shutil.move(i, Good_Male)
                    elif json_face['beauty'] < 60:
                        shutil.move(i, Normal_Male)
                elif json_face['gender']['type'] == 'female':
                    if json_face['beauty'] >= 60:
                        shutil.move(i, Good_Female)
                    elif json_face['beauty'] < 60:
                        shutil.move(i, Normal_Female)
                print(
                    i[-12:][:9],
                    json_face['gender']['type'], json_face['gender']['probability'],
                    json_face['age'],
                    json_face['beauty'],
                    json_face['face_shape']['type'], json_face['face_shape']['probability'],
                    json_face['expression']['type'], json_face['expression']['probability'],
                    json_face['glasses']['type'], json_face['glasses']['probability'],
                    json_face['race']['type'], json_face['race']['probability'],
                    file=txt
                )
                print(num, i, i[-12:-4], add_user['error_msg'], add_user['log_id'])
            except:
                size = os.path.getsize(i)
                if size == 681:
                    shutil.move(i, NaN)
                print(num, i+'*')

        print('--- All finished ---')


if __name__ == '__main__':
    l = input('Please input path you want to analysis:')
    bfi = BaiduFaceIdentify()
    bfi.parse_face_pic(l)
