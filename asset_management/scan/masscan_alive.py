import masscan


# perform a network scan with nmap
def scanNetwork(network):
    hosts = []
    nm = masscan.PortScanner()
    a = nm.scan(hosts=network, arguments='--ping --rate 2000')
    print(a)
    for k, v in a['scan'].items():
        hosts.append(k)
        print(k)
        print(v)
    return hosts


if __name__ == '__main__':
    network = '192.168.163.0/24'
    print(scanNetwork(network))

    hosts = ['10.12.189.196', '10.12.189.204', '10.12.189.28', '10.12.189.78', '10.12.189.225', '10.12.189.115',
             '10.12.189.206', '10.12.189.31', '10.12.189.29', '10.12.189.73', '10.12.189.188', '10.12.189.66',
             '10.12.189.190', '10.12.189.238', '10.12.189.50', '10.12.189.182', '10.12.189.146', '10.12.189.46',
             '10.12.189.167', '10.12.189.94', '10.12.189.212', '10.12.189.53', '10.12.189.161', '10.12.189.130',
             '10.12.189.147', '10.12.189.129']

