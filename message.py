FLOW_TYPE_DDOS = 0
FLOW_TYPE_WEBSHELL = 1
FLOW_TYPE_BOTNET = 2
FLOW_TYPE_TROJAN = 3
FLOW_TYPE_WORM = 4
FLOW_TYPE_VIRUS = 5
FLOW_TYPE_SQLINJECT = 6
FLOW_TYPE_XMLINJECT = 7
FLOW_TYPE_XSS = 8
FLOW_TYPE_PORTSCAN = 9
class AbnormalTraffic:
    def __init__(self, type, time, src, dst, detail):
        self.type = type  # 类型（10种）
        self.time = time  # 发生时间
        self.src_ip = src  # 源IP
        self.dst_ip = dst  # 目的IP
        self.detail = detail  # 详细信息
    def obj(self):
        return { "type": self.type, "time": str(self.time), "src": self.src_ip, "dst": self.dst_ip, "detail": str(self.detail)}
class AbnormalHostMSG:
    def __init__(self, ip, name, detail, time):
        self.ip = ip
        self.name = name
        self.detail = detail
        self.time = time
    def obj(self):
        return { "ip": self.ip, "name": self.name, "time": str(self.time), "detail": str(self.detail)}


MSG_TYPE_TRAFFIC = 0
MSG_TYPE_HOST = 1
MSG_TYPE_USER = 2
class AbnormalEventMSG:
    def __init__(self, type, data) -> None:
        self.type = type
        self.data = data
