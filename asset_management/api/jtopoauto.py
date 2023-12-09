# 根据数据库中的内容自动生成Jtopo文件
from IPy import IP
import json
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from http import HTTPStatus
from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES

from asset_management.tools.jtopotools import *
from asset_management.models import *
from rest_framework.response import Response

# 自动生成拓扑图的逻辑如下：
# 首先根据用户输入的网段10.12.189.0/24划分成8个子网段，分别为10.12.189.0/27,10.12.189.32/27，......
# 建立主拓扑图，topo_id为'main'，包含8个子拓扑节点，分别对应8个子网段，写入json文件，并且子拓扑节点的id就是子网段如10.12.189.0/27，并构建子拓扑图字典
# 遍历数据库中主机信息表的所有主机，构造节点，并根据其IP将其加入对应的子拓扑字典中
# 将子拓扑字典写入json文件

# 子网划分的尾部数字，最多划分为8个子网
tails = ["0", "32", "64", "96", "128", "160", "192", "224"]
# 子网掩码
masks = ["255.255.255.0", "255.255.255.128", "255.255.255.192", "255.255.255.224"]

# TODO: 这里需要处理没有main拓扑图的情况
# mainFilepath = JtopoFilePath.objects.get(topo_id='main').topo_src
mainFilepath = 'asset_management/files/jtopo_json/topo.json'

# 存放子网段对应拓扑图字典的字典 dicts[subnet]表示子网为subnet（例如，subnet='10.12.189.0/27'）的拓扑图字典
dicts = {}


class JtopoAutoView(APIView):
    # 自动生成拓扑图的post请求
    def post(self, request):
        net = json.loads(request.body)['net']
        ips = IP(net)
        # 接受的网段类似为10.12.189.0/24
        # 截取出前三段
        # print(str(ips.net())) #10.12.189.0
        netHeader = str(ips.net())[:-1]
        # print(netHeader) #10.12.189.
        # 判断数据库中是否有该网段内的ip
        querySet = Asset.objects.filter(ip__startswith=netHeader)
        # 如果没有，则返回消息
        if len(querySet) == 0:
            # 没有ip在该网段中
            return CustomResponse(
                code=ERROR_CODES['PRECONDITION_FAILED'],
                msg=ERROR_MESSAGES['PRECONDITION_FAILED'],
                data={},
                status=HTTPStatus.PRECONDITION_FAILED
            )
        # 分成八个子网
        subnets = []
        topoIDs = {}  # 存放子拓扑图的拓扑id，就是在生成子拓扑节点时生成的nodeId
        xdict = {}  # 存放各个子网拓扑图中节点的初始横坐标x，添加节点时横坐标自增
        ydict = {}  # 存放各个子网拓扑图中节点的初始纵坐标y，添加节点时如果一行节点超过8个纵坐标自增200
        countAssetByRow = {}  # 存放各个子网拓扑图中一行的节点数量，大于8的时候换行（纵坐标ydict[subnet]+=200），横坐标归为50，并将计数归1
        for tail in tails:
            subnet = netHeader + tail + "/27"
            subnets.append(subnet)
        print('subnets:%s' % subnets)
        try:
            load_dict = generateOrdinaryDict('main')
            print("主拓扑字典已经生成")
            # load_dict=generateOrdinaryDict('')
            x = 0  # 主拓扑图中的子拓扑节点横坐标
            for subnet in subnets:
                x += 150  # 横坐标自增150
                topoNode = generateTopoNode(subnet, x)
                load_dict['topology_json']['childs'][0]['childs'].append(topoNode)
                # 将nodeId作为拓扑ID构造初始子拓扑图
                topoIDs[subnet] = topoNode['nodeId']
                dicts[subnet] = generateSubTopoDict(topoNode['nodeId'], netHeader + "0/24", "")
                xdict[subnet] = 20
                ydict[subnet] = 100
                countAssetByRow[subnet] = 0
            # 将主拓扑图写入文件
            writeJson(load_dict, mainFilepath)
        except Exception as e:
            print(e)
            # 生成主拓扑图失败
            return CustomResponse(
                code=ERROR_CODES['NOT_ACCEPTABLE'],
                msg=ERROR_MESSAGES['NOT_ACCEPTABLE'],
                data={},
                status=HTTPStatus.NOT_ACCEPTABLE
            )
        try:
            assetlist = Asset.objects.all()  # 从数据库的主机表中获取主机信息
            for asset in assetlist:
                ip = asset.ip  # 主机ip
                subnet = str(IP(ip).make_net('255.255.255.224'))  # 主机IP所在的子网段，/27形式的
                # print(subnet)
                try:
                    # 构造该ip对应的主机节点并添加到对应的子网中
                    xdict[subnet] += 130  # 横坐标自增
                    countAssetByRow[subnet] += 1  # 一行节点的数量加一
                    if countAssetByRow[subnet] > 8:
                        xdict[subnet] = 150
                        ydict[subnet] += 200
                        countAssetByRow[subnet] = 1
                    dicts[subnet]['topology_json']['childs'][0]['childs'].append(
                        generateNode(ip, xdict[subnet], ydict[subnet], asset.device_type))
                except Exception as e:
                    print(e)
                    print('ip为%s的主机不在指定网段中' % ip)
            for subnet in subnets:
                # 添加完子网的节点之后将子网拓扑图写入文件
                # 将此处的参数subnet改成子拓扑图的topo_id，对应数据库中的topo_id
                filepath = generateFilepath(topoIDs[subnet])
                writeJson(dicts[subnet], filepath)
        except Exception as e:
            print(e)
            # 生成拓扑节点出现错误
            return CustomResponse(
                code=ERROR_CODES['INTERNAL_SERVER_ERROR'],
                msg=str(e),
                data={},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
        return CustomResponse(
            data={}
        )


# def generateTopoDict(topo_id):  # 根据子网生成topo的字典
#     load_dict = generateOrdinaryDict(topo_id)
#     querySet = Asset.objects.filter(is_active=True)  # 从数据库的主机表中获取主机信息
#     maxsize = 10  # 控制节点数量
#     x = 100  # 节点横坐标
#     for asset in querySet:
#         maxsize -= 1
#         x += 50  # 新节点横坐标比上一个节点右移50
#         load_dict['topology_json']['childs'][0]['childs'].append(generateNode(asset.ip, x))
#         if maxsize == 0:
#             break
#     return load_dict
