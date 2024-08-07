import json
from flask import request, jsonify
from app.cores.base.modle.devices_modle import devices_list, devices_ota_data
from app.cores.base.common.ota_api import check_deviceid
from app.routes.view import bp

@bp.route('/api/add_device', methods=['POST'])
def add_device():
    data = json.loads(request.data)
    productId = data['productId']
    device_did = data['device_did']
    resourceName = data['resourceName']
    environment = data['environment']
    update_version = data['update_version']
    demote_version = data['demote_version']
    count = data['count']
    if productId and device_did and resourceName and environment and update_version and demote_version and count:
        if check_deviceid(device_did, environment):
            devices_list.add_device(productId, device_did, resourceName, environment, update_version, demote_version, count)
            return jsonify(code=200, msg="添加成功")
        else:
            return jsonify(code=500, msg="did输入不符,请检查")
    else:
        return jsonify(code=500, msg="数据不可为空")

@bp.route('/api/get_devices', methods=['GET'])
def get_devices_data():
    device_did = request.args.get('device_did')
    if not device_did:
        return {"msg": "参数为空"}, 500
    device_data = devices_list.query_device(device_did)
    if not device_data:
        return {"msg": "没有该数据"}, 500
    else:
        for device in device_data:
            device_info = {
                "product_id": device.productId,
                "resourceName": device.resourceName,
                "environment": device.environment,
                "update_version": device.update_version,
                "demote_version": device.demote_version,
                "count": device.count
            }
            return jsonify(data=device_info), 200


@bp.route('/api/add_device_data', methods=['POST'])
def add_device_data():
    device_data = json.loads(request.data)
    device_id = device_data['device_did']
    filesize = device_data['filesize']
    versionName = device_data['versionName']
    file_url = device_data['file_Url']
    md5 = device_data['md5']
    sha256 = device_data['sha256']
    version = device_data['version']
    if device_id and filesize and md5 and versionName and file_url:
        devices_ota_data.add_ota_data(device_id, filesize, versionName, file_url, md5, sha256, version)
        return jsonify(code=200, msg="添加成功")
    else:
        return jsonify(code=500, msg="数据不可为空")

@bp.route('/api/get_device_data', methods=['GET'])
def get_device_data():
    device_did = request.args.get('device_did')
    version = request.args.get('version')
    if not device_did and not version:
        return {"msg": "参数为空"}, 500
    device_ota_data = devices_ota_data.query_data_by_device_did(device_did, version)
    if not device_ota_data:
        return {"msg": "没有该数据"}, 500
    else:
        device_ota_data_list = []
        for device in device_ota_data:
            device_info = {
                "device_did": device.device_did,
                "file_size": device.filesize,
                "md5": device.md5,
                "sha256": device.sha256,
                "version": device.version,
                "versionName": device.versionName,
            }
            device_ota_data_list.append(device_info)
        return jsonify(data=device_ota_data_list), 200
