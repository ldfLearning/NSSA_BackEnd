import nmap
import threading
import time

from nmap_alive import scanNetwork
from singleScan import singleScan


class myThread(threading.Thread):
    def __init__(self, threadID, host, arguments):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host = host
        self.arguments = arguments
        self.info = {}

    def run(self):
        print("start scan: " + self.host)
        self.info = singleScan(self.host, self.arguments)

    def get_result(self):
        return self.info


def multiScan(network, arguments = '-sV -O -T4'):
    print('network: ' + network)
    hosts = scanNetwork(network)
    threads = []
    i = 1
    for host in hosts:
        # 创建新线程
        newthread = myThread(i, host, arguments)
        # 开启新线程
        newthread.start()
        threads.append(newthread)
        i += 1
    # 等待所有线程完成
    for t in threads:
        t.join()
    # 收集结果
    infos = []
    for t in threads:
        info = t.get_result()
        if info != {}:  # info不为空，当前主机是存活状态，入表，否则当前主机不是存活状态
            infos.append(info)
    print(f"扫描完成，得到{len(infos)}条主机信息，退出主线程")
    # print(infos)
    return infos


if __name__ == "__main__":
    network = '192.168.163.0/24'
    multiScan(network)
