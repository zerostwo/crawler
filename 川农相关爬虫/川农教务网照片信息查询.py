import requests
import json

class Faceset():
    def get_access_token(self):
        client_id = 'G9yWRpQRxqGLl0vZv2MIqoNE'                # 此变量赋值成自己API Key的值
        client_secret = 'RLol5YGP3EUIEgmQskKLScYvUm3cySvx'    # 此变量赋值成自己Secret Key的值
        auth_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret

        response_at = requests.get(auth_url)
        json_result = json.loads(response_at.text)
        access_token = json_result['access_token']
        return access_token

    def get_info(self, uid, group_id, url_fi):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        post_data = {
            'uid': uid,
            'user_id': uid,
            'group_id': group_id
        }
        response_fi = requests.post(url_fi, headers=headers, data=post_data)
        json_fi_result = json.loads(response_fi.text)
        return json_fi_result

    def parse_face_pic(self):
        access_token = self.get_access_token()
        url_fi = 'https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get?access_token=' + access_token
        i = 1
        while i == 1:
            id = input('Please input user id you want to ask:')
            id_group = input('Please input user group you want to ask:')
            try:
                json_faces = self.get_info(id, id_group, url_fi)
                print(json_faces['result']['user_list'][0]['user_info'])
                i = int(input('Go on? If go on, inputing 1; If not, inputing 2:'))
            except:
                print("--- There is no %s in faceset, please re-enter ---" % id)
                i = int(input('Go on? If go on, inputing 1; If not, inputing 2:'))


if __name__ == '__main__':
    bfi = Faceset()
    bfi.parse_face_pic()
