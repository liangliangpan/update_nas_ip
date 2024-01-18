import socket,json,os
import requests
from datetime import datetime

url_to_send = open('url.txt', 'r').read()

def get_ipv6_address():
    s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    try:
        # 这里使用Google的公共DNS服务器地址和端口
        s.settimeout(3)
        s.connect(('2001:4860:4860::8888', 80))
        return s.getsockname()[0]
    finally:
        s.close()

def send_string_to_server(url, data):
    response = requests.post(url, data=data)
    print(response.text)

def get_previous_addr(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
            return json.loads(data)
    else:
        return None

def write_data_to_file(file_path,data):
    with open(file_path, 'w') as file:
        file.write(data)

def main():
    file_path = 'ip_data.json'
    ip_prev = get_previous_addr(file_path)
    ip_addr = get_ipv6_address()
    current_time = str(datetime.now())
    new_ip={'ip':ip_addr,'device':'nas','update_time':current_time}
    
    if ip_prev == None or ip_prev['ip'] != new_ip['ip']:
        print(current_time + '| update to new ip: ['+ip_addr+']')
        write_data_to_file(file_path,json.dumps(new_ip))
        send_string_to_server(url_to_send, json.dumps(new_ip))
    else:
        print(current_time + '| no need to update ip')

if __name__ == '__main__':
    main()
