import json
from app.cores.base.common.request import Post, Get
from app.cores.base.common.request_util import handle_url, handle_version_and_path, handle_now_versionName

test_domain = '10.60.2.114'
test_port = 31893
pro_domain = '10.50.2.64'
pro_port = 32573


class Ota_Api:
    resourceName = None
    environment = None

    def get_token(self):
        url = handle_url('https', 'shenyu.lingdong.cn', '', '/passport/lingdong/oauth2/token')
        payload = {
            "client_id": "6c78ee67-1716-4c99-af3b-51bff44745b7",
            "grant_type": "password",
            "username": "13380917781",
            "password": "dc483e80a7a0bd9ef71d8cf973673924",
            "login_type": "password",
            "captcha_scene": "login"
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = Post(url, data=payload, headers=headers).send()
        token_data = json.loads(res.text)
        if token_data['code'] == 'SUCCESS':
            return token_data['data']['access_token']

    def get_device_data(self, pid, version):
        url = ("https://aiot.aciga.com.cn/xspec/v1/resources?productId={}"
               "&resourceName={}&productVersion=0&userdebug=true").format(
            pid, self.resourceName)
        res = Get(url=url).send()
        data = json.loads(res.text)
        file_url, filesize, md5, sha256 = handle_version_and_path(data, version)
        return file_url, filesize, md5, version, sha256

    def action(self, did, file_url, filesize, md5, version, sha256):
        path = '/api/v1/internal/invoke-actions'
        url = None
        if self.environment == 'test':
            url = handle_url('http', test_domain, test_port, path)
        elif self.environment == 'pro':
            url = handle_url('http', pro_domain, pro_port, path)
        json_data = json.dumps({"devices": [
            {
                "did": did,
                "actions": [
                    {
                        "aid": "{}.5.1".format(did),
                        "in": [
                            {
                                "piid": 7,
                                "values": [
                                    [
                                        {
                                            "piid": 1,
                                            "value": "3"
                                        },
                                        {
                                            "piid": 3,
                                            "value": md5
                                        },
                                        {
                                            "piid": 6,
                                            "value": file_url
                                        },
                                        {
                                            "piid": 9,
                                            "value": "mcu"
                                        },
                                        {
                                            "piid": 10,
                                            "value": filesize
                                        },
                                        {
                                            "piid": 4,
                                            "value": sha256
                                        },
                                        {
                                            "piid": 5,
                                            "value": version
                                        }
                                    ]
                                ]
                            },
                            {
                                "piid": 9,
                                "values": [
                                    "mcu"
                                ]
                            },
                            {
                                "piid": 11,
                                "values": [
                                    did
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
        })
        res = Post(url, data=json_data).send()
        data = json.loads(res.text)
        return data['code']

    def read(self, did):
        path = '/api/v1/internal/get-properties'
        url = None
        if self.environment == 'test':
            url = handle_url('http', test_domain, test_port, path)
        elif self.environment == 'pro':
            url = handle_url('http', pro_domain, pro_port, path)
        json_data = json.dumps({"devices": [
            {
                "did": did,
                "properties": [
                    "{}.1.1".format(did)
                ]
            }
        ]
        })
        res = Post(url, data=json_data).send()
        data = json.loads(res.text)
        version = handle_now_versionName(data)
        return version


def check_deviceid(did, environment):
    Ota_Api.environment = environment
    check = Ota_Api().read(did)
    if not check:
        return False
    else:
        return True

if __name__ == '__main__':
    Ota_Api.environment = "pro"
    Ota_Api().read('xw8h5HrZ')