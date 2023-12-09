# 与前端交互网络拓扑json数据
import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from asset_management.tools.jtopotools import *
from asset_management.models import *
from rest_framework.response import Response

class JtopoView(APIView):
#
    def get(self, request):
        query = request.query_params.dict()
        topo_id = query['id']  # 请求参数中topo图的id
        filepath = getFilepath(topo_id)
        if filepath == '':
            # 获取拓扑图路径失败
            return CustomResponse(
                code=ERROR_CODES['BAD_REQUEST'],
                msg=ERROR_MESSAGES['BAD_REQUEST'],
                data={},
                status=HTTPStatus.BAD_REQUEST
            )
        try:
            # load_dict = generateTopoDict()
            # load_dict = readJson(filepath)
            # load_dict["AssetList"] = generateDeviceList()
            # writeJson(load_dict, filepath)
            print('正在读取拓扑图')
            load_dict = readJson(filepath)
            # 由于有多张拓扑图，每次获取拓扑图都从数据库里读取设备列表
            load_dict['AssetList'] = generateDeviceList()
            writeJson(load_dict, filepath)
            # res['data'] = load_dict
        except Exception as e:
            print(e)
            # 获取网络拓扑失败
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return CustomResponse(
            data=load_dict
        )
        # filepath = "static/topo.json"
        # load_dict = readJson(filepath)
        # load_dict["AssetList"] = generateDeviceList()
        # writeJson(load_dict, filepath)
        # res['data'] = readJson(filepath)

    # post中实现判断子拓扑节点的id是否存在于数据库中，如果不存在就要创建对应的拓扑文件
    def post(self, request):
        data = json.loads(request.body)  # 前端传过来数据的为字符串，需要解析为json
        filepath = getFilepath(data['topology_id'])
        if filepath == '':
            # 拓扑id有误
            return CustomResponse(
                code=ERROR_CODES['NOT_ACCEPTABLE'],
                msg=ERROR_MESSAGES['NOT_ACCEPTABLE'],
                data={},
                status=HTTPStatus.NOT_ACCEPTABLE
            )
        try:
            # 保存拓扑图并不改变设备列表
            load_dict = readJson(filepath)
            load_dict['topology_json'] = json.loads(data['topology_json'])
            load_dict['topology_id'] = data['topology_id']
            print('完成拓扑图修改的保存')
            # 检查拓扑图文件中的子拓扑节点
            if not checkNode(load_dict):
                # 创建子拓扑图失败
                return CustomResponse(
                    code=ERROR_CODES['NOT_ACCEPTABLE'],
                    msg=ERROR_MESSAGES['NOT_ACCEPTABLE'],
                    data={},
                    status=HTTPStatus.NOT_ACCEPTABLE
                )
            writeJson(load_dict, filepath)  # 完成拓扑文件的保存
            # res['data'] = readJson(filepath)
            # res['data'] = load_dict
        except Exception as e:
            print(e)
            # 保存网络拓扑失败
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return CustomResponse(
            data=load_dict
        )


# 实现与前端交互jtopo的网络拓扑json文件,包括读取和写入json文件
# 后续需要添加根据扫描结果生成节点的方法

# 逻辑是将设备列表和topo图分开，对拓扑图修改和添加设备都会改变Json文件
# 用户添加新设备，前端将添加的新设备信息传过来，后端经过处理存到数据库，
# 并修改json文件（是仅仅修改设备列表还是整个修改？前端仍需要将当前拓扑图传过来？涉及到是否只有按保存按钮才能保存拓扑图的问题）
