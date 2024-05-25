import os
import sys
import signal
import time
import socket
import re
import glob
import shutil
import platform
import subprocess

#检查是否有result.csv文件,有则删除
if os.path.exists('result.csv'):
    os.remove('result.csv')

def signal_handler(sig, frame):
    sys.exit(0)

tll = None
tl = None
sl = None
debug = False

if len(sys.argv) > 1:
    if sys.argv[1] == '-h':
        print('Usage: python main.py [-h] [-tll] [-tl] [-sl] [--debug]')
        print('Options:')
        print('  -h, --help  show this help message and exit')
        print('  -tll        设置最大延迟')
        print('  -tl         设置最小延迟')
        print('  -sl         下载速度下限')
        print('  --debug     输出命令执行结果')
        sys.exit(0)
    elif sys.argv[1] == '-tll':
        tll = sys.argv[2]
    elif sys.argv[1] == '-tl':
        tl = sys.argv[2]
    elif sys.argv[1] == '-sl':
        sl = sys.argv[2]
    elif sys.argv[1] == '--debug':
        debug = True

signal.signal(signal.SIGINT, signal_handler)

ip_port_list = []
with open('list.txt', 'r') as f:
    for line in f.readlines():
        ip_port = line.strip()
        if not ip_port:
            continue
        if 'https://' in ip_port:
            ip_port = ip_port.replace('https://', '')
        if re.match(r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,6}$', ip_port):
            try:
                ip = socket.gethostbyname(ip_port)
                ip_port = ip+':443'
            except socket.gaierror:
                pass
        elif ':' not in ip_port:
            ip_port += ':443'
        if 'http://' in ip_port:
            ip_port = ip_port.replace('http://', '')
        ip_port_list.append(ip_port)

port_list = []
for ip_port in ip_port_list:
    ip, port = ip_port.split(':')
    if port not in port_list:
        port_list.append(port)

port_ip_dict = {}
for port in port_list:
    ip_list = []
    for ip_port in ip_port_list:
        ip, p = ip_port.split(':')
        if p == port:
            ip_list.append(ip)
    port_ip_dict[port] = ip_list

print('共有', len(port_list), '个端口')

for port, ip_list in port_ip_dict.items():
    print('端口' ,port ,"有", len(ip_list),"个ip")
    with open('ip.txt', 'w') as f:
        for ip in ip_list:
            f.write(ip+'\n')
    command = './CloudflareST -o result_'+port+'.csv -tp '+port+' -url https://cdn.cloudflare.steamstatic.com/steam/apps/256843155/movie_max.mp4 --httping'
    if tll:
        command += ' -tll ' + tll
    if tl:
        command += ' -tl ' + tl
    if sl:
        command += ' -sl ' + sl
    if platform.system() == 'Windows':
        command = command.replace('./CloudflareST', '.\\CloudflareST.exe')
    
    if debug:
        subprocess.call(command, shell=True)
    else:
        if platform.system() == 'Windows':
            subprocess.call(command + " >nul 2>&1", shell=True)
        else:
            subprocess.call(command + " > /dev/null 2>&1", shell=True)

    if not os.path.exists('result_'+port+'.csv'):
        print('端口', port, '无结果')
    time.sleep(2)

with open('result_1.csv', 'w') as f:
    f.write('IP 地址,已发送,已接收,丢包率,平均延迟,下载速度 (MB/s)\n')

filenames = ['result_1.csv'] + [name for name in glob.glob('result_*.csv') if name not in ['result.csv', 'result_1.csv']]

with open('result.csv', 'wb') as wfd:
    for filename in filenames:
        with open(filename, 'rb') as fd:
            if filename != 'result_1.csv':
                fd.readline()
            shutil.copyfileobj(fd, wfd)

for filename in glob.glob('result_*.csv'):
    os.remove(filename)