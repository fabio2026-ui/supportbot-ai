#!/usr/bin/env python3
"""
测试公网访问脚本
检查服务是否可以从外部访问
"""

import socket
import requests
import time

def check_port(host, port, timeout=2):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def check_http_service(host, port, path="/", timeout=3):
    """检查HTTP服务是否响应"""
    try:
        url = f"http://{host}:{port}{path}"
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False

def main():
    print("🔍 测试公网访问状态")
    print("=" * 50)
    
    # 测试本地访问
    print("\n📊 本地访问测试 (容器内部):")
    ports = [
        (8082, "AI游戏商店"),
        (5010, "支付系统"),
        (5020, "备用端口")
    ]
    
    for port, service in ports:
        local_open = check_port("localhost", port)
        if local_open:
            print(f"✅ 端口 {port} ({service}) - 本地监听正常")
            if port in [8082, 5010]:
                http_ok = check_http_service("localhost", port)
                if http_ok:
                    print(f"   ✅ HTTP服务响应正常")
                else:
                    print(f"   ⚠️  HTTP服务无响应")
        else:
            print(f"❌ 端口 {port} ({service}) - 本地未监听")
    
    # 测试外部IP访问
    print("\n🌐 外部访问测试:")
    
    # 获取外部IP
    try:
        external_ip = requests.get("https://api.ipify.org", timeout=5).text
        print(f"外部IP地址: {external_ip}")
        
        for port, service in ports:
            if port == 5020:  # 跳过未使用的端口
                continue
                
            external_open = check_port(external_ip, port, timeout=5)
            if external_open:
                print(f"✅ 端口 {port} ({service}) - 外部访问正常")
                http_ok = check_http_service(external_ip, port, timeout=5)
                if http_ok:
                    print(f"   ✅ 外部HTTP服务响应正常")
                else:
                    print(f"   ⚠️  外部HTTP服务无响应")
            else:
                print(f"❌ 端口 {port} ({service}) - 外部访问被阻止")
                print(f"   原因: 防火墙/安全组/端口映射未配置")
    except Exception as e:
        print(f"⚠️  无法获取外部IP: {e}")
    
    print("\n🔧 解决方案:")
    print("1. 检查Docker端口映射: docker ps --format 'table {{.Names}}\t{{.Ports}}'")
    print("2. 检查宿主机防火墙: sudo ufw status")
    print("3. 检查云服务商安全组配置")
    print("4. 如果需要，重新运行容器并映射端口:")
    print("   docker run -d -p 8082:8082 -p 5010:5010 -p 5020:5020 ...")

if __name__ == "__main__":
    main()