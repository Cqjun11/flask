import json
from app.cores.base.common.ota_api import read, get_device_data


def asser_data(data):
    json_data = json.loads(data)
    if not json_data:
        return False
    else:
        return True

def check_deviceid(did):
    check = read(did)
    if not check:
        return False
def check_device_data(pid, version):
    check = get_device_data(pid, version)
    if not check:
        return False
