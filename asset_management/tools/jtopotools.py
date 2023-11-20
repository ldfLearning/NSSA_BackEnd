import json
import uuid

from asset_management.models import *

# 主机类型与其图片和描述文字的映射
typeToImg = {"server": ["icon_server.png", "服务器"], "router": ["icon_router.png", "路由器"],
             "firewall": ["icon_firewall.png", "防火墙"], "ips": ["icon_ips.png", "入侵防御系统"], }


# 根据topo图的id获取拓扑图路径，如果返回的结果为''，说明获取路径失败
def getFilepath(topo_id):
    filepath = ''
    if len(topo_id) == 0:
        # id长度为0，表示请求的是主拓扑图
        try:
            print('请求的是主拓扑图')
            filepath = JtopoFilePath.objects.get(topo_id='main').topo_src
        except Exception as e:
            print(e)
            print('获取主拓扑图路径失败')
    else:
        # 否则在数据库中找到id对应的拓扑图路径
        try:
            filepath = JtopoFilePath.objects.get(topo_id=topo_id).topo_src
        except Exception as e:
            print(e)
            print('获取拓扑图路径失败')
    return filepath


# 根据拓扑id生成文件名
def generateFilepath(topo_id):
    try:
        print("在数据库中寻找topoid:%s" % topo_id)
        filepath = JtopoFilePath.objects.get(topo_id=topo_id).topo_src
    except Exception as e:
        # 数据库中不存在对应的topo_id，在数据库中新添加topo_id
        JtopoFilePath.objects.create(topo_id=topo_id, topo_src='')
        print('创建新的topo，其topo_id为%s' % topo_id)
        topo = JtopoFilePath.objects.get(topo_id=topo_id)
        filepath = 'asset_management/files/jtopo_json/' + str(topo.id) + '.json'  # 新增的topo文件的命名，使用数据库中自增主键id加上.json
        print('新建的拓扑文件路径为：%s' % filepath)
        topo.topo_src = filepath
        topo.save()
    return filepath


# 检查拓扑图中的子拓扑图节点，如果该节点id在数据库中不存在，则将其入库，并创建对应的json文件
def checkNode(load_dict):
    for node in load_dict['topology_json']['childs'][0]['childs']:
        # 如果是子拓扑节点
        if node['elementType'] == 'node' and node['nodeType'] == 'TOPOLOGY':
            topo_id = node['nodeId']
            # 获取topo_id对应的文件路径
            # 创建相应的topo文件
            # 这时的子拓扑图是最初始状态的
            try:
                print("在数据库中寻找topoid:%s" % topo_id)
                JtopoFilePath.objects.get(topo_id=topo_id)
            except Exception as e:
                # 数据库中不存在对应的topo_id，在数据库中新添加topo_id
                JtopoFilePath.objects.create(topo_id=topo_id, topo_src='')
                print('创建新的topo，其topo_id为%s' % topo_id)
                topo = JtopoFilePath.objects.get(topo_id=topo_id)
                filepath = 'asset_management/files/jtopo_json/' + str(topo.id) + '.json'  # 新增的topo文件的命名，使用数据库中自增主键id加上.json
                print('新建的拓扑文件路径为：%s' % filepath)
                topo.topo_src = filepath
                topo.save()
                # 生成子拓扑图的字典
                topo_dict = generateSubTopoDict(topo_id, "", load_dict['topology_id'])
                try:
                    # 写入文件
                    # print('写入文件之前的filepath为：%s' % filepath)
                    writeJson(topo_dict, filepath)
                    # print('写入文件完成')
                except Exception as e:
                    print(e)
                    print('新建子拓扑图失败')
                    return False
    return True


def writeJson(load_dict, filepath):
    with open(filepath, "w", encoding='utf-8') as f:
        # json.dump(dict_, f) # 写为一行
        json.dump(load_dict, f, indent=2, sort_keys=True, ensure_ascii=False)  # 写为多行
    f.close()


def readJson(filepath):
    with open(filepath, encoding="utf-8") as f:
        load_dict = json.load(f)
        return load_dict
    f.close()


# 生成topo的字典，最初始状态
def generateOrdinaryDict(topo_id):
    load_dict = {"ImgList": ["asset_management/files/jtopo_img/icon_server.png",
                             "asset_management/files/jtopo_img/icon_access_switch.png",
                             "asset_management/files/jtopo_img/icon_router.png",
                             "asset_management/files/jtopo_img/icon_ips.png",
                             "asset_management/files/jtopo_img/icon_balancing.png"],
                 "topology_id": topo_id,
                 "topology_json": {
                     "version": "0.4.8",
                     "wheelZoom": 0.95,
                     "width": 910,
                     "height": 599,
                     "id": "ST172.19.105.52015100809430700001",
                     "childs": [
                         {
                             "elementType": "scene",
                             "id": "S172.19.105.52015100809430700002",
                             "translateX": 133.5,
                             "translateY": -43,
                             "scaleX": 1,
                             "scaleY": 1,
                             "childs": [],
                         }]
                 },
                 'AssetList': generateDeviceList()}
    return load_dict


def generateDeviceList():
    deviceList = []
    deviceList.append(generateDevice("服务器设备"))
    deviceList.append(generateDevice("网络设备"))
    deviceList.append(generateDevice("安全设备"))
    deviceList.append(generateDevice("其他设备"))
    return deviceList


# 根据设备类型从数据库中取设备列表
def generateDevice(type):
    list = []
    try:
        querySet = JtopoDevices.objects.filter(type=type)
        # print(querySet)
        for device in querySet:
            list.append({"imgUrl": device.imgUrl, "name": device.name, "title": device.title})
    except Exception as e:
        print(e)
    return {"type": type, "list": list}


def generateSubTopoDict(topo_id, ip, nodeId):
    load_dict = generateOrdinaryDict(topo_id)
    load_dict['topology_json']['childs'][0]['childs'].append(generateUpStreamNode(ip, nodeId))
    return load_dict


# 生成子拓扑节点
def generateTopoNode(subnet, x):
    # 子拓扑的ID设置为子网段
    node = {"elementType": "node", "height": 32, "id": subnet, "layout": "",
            "nodeId": str(uuid.uuid4()),
            "nodeImage": "icon_universal_service.png",
            "nodeParams": "", "nodeType": "TOPOLOGY", "rotate": 0, "scaleX": 1, "scaleY": 1, "text": "子拓扑" + subnet,
            "textPosition": "Bottom_Center", "visible": True, "width": 32, "x": x, "y": 216.01, "zIndex": 3,
            }
    print(node)
    return node


def generateUpStreamNode(ip, nodeId):  # 生成上一层网络的节点，ip是上一层的id，nodeId是上一层拓扑图的nodeId
    node = {"elementType": "node",
            "height": 32,
            "id": ip,
            "layout": "",
            "nodeId": nodeId,
            "nodeImage": "icon_upstream.png",
            "nodeParams": "",
            "nodeType": "UPSTREAM",
            "rotate": 0,
            "scaleX": 1,
            "scaleY": 1,
            "text": "上一层网段",
            "textPosition": "Bottom_Center",
            "visible": True,
            "width": 32,
            "x": 340,
            "y": -20,
            "zIndex": 3, }

    # 设置节点的文本为上一层网络和其ip
    node['text'] += ip
    print(node)
    return node


# TODO 生成节点时，nodeID设置成不一样的，暂时将其设置为IP
def generateNode(ip, x, y, hostType):  # 根据IP地址生成节点，默认是服务器类型，通过横坐标来区别不同节点的位置
    # 普通主机节点
    node = {"elementType": "node",
            "height": 32,
            "id": ip,
            "layout": "",
            # "nodeId": "fea97fc6-f3ac-4e97-8e3c-6d19dbfc7256",
            # 随机生成nodeId
            "nodeId": str(uuid.uuid4()),
            "nodeImage": "icon_server.png",
            "nodeParams": "",
            "nodeType": "PM",
            "rotate": 0,
            "scaleX": 1,
            "scaleY": 1,
            "text": "服务器",
            "textPosition": "Bottom_Center",
            "visible": True,
            "width": 32,
            "x": x,
            "y": y,
            "zIndex": 3, }
    try:
        nodeImage = typeToImg[hostType][0]
        text = typeToImg[hostType][1]
    except Exception as e:
        print(e)
        # 默认主机类型是服务器
        nodeImage = typeToImg['server'][0]
        text = typeToImg['server'][1]
    node['nodeImage'] = nodeImage
    # 设置节点的文本为节点对应的设备和其ip
    node['text'] = text + ip
    return node
