import json
from app.cores.base.common.ota_api import Ota_Api
from app.cores.base.common.request import Post, Get
from app.cores.base.common.request_util import handle_url


class hand_ota(Ota_Api):
    def __init__(self, device_did):
        self.ota_api = Ota_Api()
        self.device_id = device_did

    def get_devices_data(self):
        find_url = handle_url('http', '127.0.0.1', '5000',
                              '/api/get_devices?device_did={}'.format(self.device_id))
        res = Get(find_url).send()
        data = json.loads(res.text)
        productId = data['product_id']
        resourceName = data['resourceName']
        environment = data['environment']
        update_version = data['update_version']
        demote_version = data['demote_version']
        Ota_Api.resourceName = resourceName
        update_file_url, update_filesize, update_md5, update_version, update_sha256 = (
            self.ota_api.get_device_data(productId, update_version))
        demote_file_url, demote_filesize, demote_md5, demote_version, demote_sha256 = (
            self.ota_api.get_device_data(productId, demote_version))

        add_data_url = handle_url('http', '127.0.0.1', '5000',
                                  '/api/add_device_data')
        update_data = json.dumps({
            "device_did": self.device_id,
            "filesize": update_filesize,
            "md5": update_md5,
            "sha256": update_sha256,
            "versionName": update_version,
            "file_Url": update_file_url,
            "version": 0
        })

        demote_data = json.dumps({
            "device_did": self.device_id,
            "filesize": demote_filesize,
            "md5": demote_md5,
            "sha256": demote_sha256,
            "versionName": demote_version,
            "file_Url": demote_file_url,
            "version": 1
        })
        update_data_res = Post(add_data_url, data=update_data).send()
        demote_data_res = Post(add_data_url, data=demote_data).send()
        print(update_data_res)

    def start_ota(self, version):
        url = handle_url('http', '127.0.0.1', '5000',
                        '/api/get_device_data?device_did={}'.format(self.device_id))
        res = Get(url).send()
        data = json.loads(res.text)
        if version:
            pass


if __name__ == '__main__':
    hand_ota('xw8h5HrZ').get_devices_data()
