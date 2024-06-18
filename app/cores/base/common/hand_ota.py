import json
from app.cores.base.common.ota_api import get_device_data
from app.cores.base.common.request import Post, Get
from app.cores.base.common.request_util import handle_url

def get_devices_data(device_did):
    find_url = handle_url('http', '127.0.0.1', '5000', '/api/get_devices?device_did={}'.format(device_did))
    res = Get(find_url).send()
    data = json.loads(res.text)
    print(data)
    productId = data['product_id']
    update_version = data['update_version']
    demote_version = data['demote_version']
    update_file_url, update_filesize, update_md5, update_sha256 = get_device_data(pid=productId,version=update_version)
    print(update_file_url, update_filesize, update_md5)
    demote_file_url, demote_filesize, demote_md5, demote_sha256 = get_device_data(pid=productId,version=demote_version)
    print(demote_file_url, demote_filesize, demote_md5, demote_sha256)

    # add_url = handle_url('http', '127.0.0.1', '5000', '')



get_devices_data('xw8h5HrZ')