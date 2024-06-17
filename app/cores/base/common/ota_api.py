import json
from app.cores.base.common.request import Post, Get
from app.cores.base.common.request_util import handle_url, handle_version_and_path, handle_now_versionName

test_domain = '10.60.2.114'
test_port = 31893
pro_domain = '10.50.2.64'
pro_port = 32573
cookie = 'idToken=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiI2MDIxOTI4NTk0OTY0NDgiLCJ4LXRlbmFudC1pZCI6MSwieC11c2VyLWlkIjo2MDIxOTI4NTk0OTY0NDgsInVzZXJOYW1lIjoi6ZmI6bqS6ZKnIiwiZXhwIjoxNzE4Njk0NzIxfQ.Ly2Yig6yHkvK16mlFGef0YZlDJdGaLFgBdTJPhMWUKb3gym2g3bIzTpwyj6WSp1O6yPMra0xNo_iCGBb3wu2RsPNaETart7lxF4E9zTGVjNRaXfztpsU9CL5V1uRpyAaWSNY6OLDBm2nn0ZovqxhfR21gVoVsIoQDS1A9Sp8pRcaZh0OyrCIovEJisDHETIQwf5vWEVwVOJQkmwbD8sCRTRWMWc8sLK50n2kPeqmdr5CPdil_k3zHvuhLsvYPOrvtQ9xg0AvYDGP9X20Zz0XXNsY2D73ONPpc-4WseqPGbPzK74qzehw9j4Q3aqOw3fwgW1M4bshtEm1gudrgZK4m9yLGTU8yoJlaRaI5L_f2UEyjVqkpl4fcQrmtw9fuIPQLJatjmQa2BZZ7qCGEZnzdFIAWh7bBV7UogpFUhVJyQfAKDd7ORYwaiHd5iP9Wm-0U16QHWKBDlAf-NpWHZ5ZQ3vI5G8h2Z2Ec2HXzfE2E81wwklmIZnGHhVuiz7N9xZIX8ppsk_QpTIYFWfyRLZxAN2DXreKaL09nqwLCsuEhNp9mwwQUIm80Dw5Rg_AVIc38PH4OvzYrQScq1JqJf79SoQAT-MogbsaP2KDUbqreGMfzq9_51VfweLNrcE5vjk_huQLHWBb_luR0Qx1ILCdxBX8hhXi66DY8QYIpEB6o9w'


def get_device_data(pid, version):
    url = "https://api-xiot.lingdong.cn/product/v1/product/resource/list?organizationCode=aciga&productId={}".format(
        pid)
    headers = {'Cookie': cookie}
    res = Get(url=url, headers=headers).send()
    data = json.loads(res.text)
    file_url, filesize, md5, version, sha256 = handle_version_and_path(data, version)
    return file_url, filesize, md5, version, sha256


def action(did, file_url, filesize, md5, version, sha256):
    path = '/api/v1/internal/invoke-actions'
    url = handle_url('http', test_domain, test_port, path)
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


def read(did):
    path = '/api/v1/internal/get-properties'
    url = handle_url('http', test_domain, test_port, path)
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

# read('xw8h5Hr')