import json
from app.cores.base.common.ota_api import Ota_Api
from app.cores.base.common.request import Post, Get
from app.cores.base.common.request_util import handle_url

class hand_ota(Ota_Api):
    def __init__(self):
        pass

    def get_devices_data(self, device_did):
        find_url = handle_url('http', '127.0.0.1', '5000', '/api/get_devices?device_did={}'.format(device_did))
        res = Get(find_url).send()
        data = json.loads(res.text)
        print(data)
        productId = data['product_id']
        resourceName = data['resource_name']
        update_version = data['update_version']
        demote_version = data['demote_version']


        # add_url = handle_url('http', '127.0.0.1', '5000', '')



get_devices_data('xw8h5HrZ')