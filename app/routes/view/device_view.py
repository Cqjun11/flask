import json
from flask import request, jsonify
from app.cores.base.modle.devices_modle import devices_list
from app.routes.view import bp

@bp.route('/add_device', methods=['POST'])
def add_device():
    data = json.loads(request.data)
    if data:
        productId = data['productId']
        device_did = data['device_did']
        update_version = data['update_version']
        demote_version = data['demote_version']
        count = data['count']
        devices_list.add_device(productId, device_did, update_version, demote_version, count)
        return jsonify(code=200, msg="添加成功")
    else:
        return jsonify(code=500, msg="数据不可为空")


# @bp.route('/delete_device', methods=['GET'])
# def delete_device():
#     return 'abc'
