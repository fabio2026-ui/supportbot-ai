#!/usr/bin/env python3
"""
检查Docker容器端口映射状态
"""

import os
import socket
import subprocess
import json

def check_port_listening(port):
    """检查端口是否在监听"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('0.0.0.0', port))
        sock.close()
        return result == 0
    except:
        return False

def check_public_access(ip, port):
    """检查公网访问"""
    try:
        import urllib.request
        import urllib.error
        import ssl
        
        # 创建不验证SSL的上下文
        context = ssl._create_unverified_context()
        
        req = urllib.request.Request(f"http://{ip}:{port}/", 
                                    headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            response = urllib.request.urlopen(req, timeout=5, context=context)
            return response.getcode() == 200
        except urllib.error.URLError as e:
            return False
    except:
        return False

def main():
    print("=== Docker容器端口映射检查 ===")
    print(f"容器内部IP: 172.17.0.2")
    print(f"公网IP: 178.104.109.237")
    print()
    
    ports_to_check = [
        (8082, "AI游戏商店"),
        (5010, "支付系统"),
        (5020, "实时演示系统")
    ]
    
    print("=== 容器内部监听状态 ===")
    for port, service in ports_to_check:
        if check_port_listening(port):
            print(f"端口 {port} ({service}): ✅ 容器内部监听正常")
        else:
            print(f"端口 {port} ({service}): ❌ 容器内部未监听")
    
    print()
    print("=== 公网访问测试 ===")
    for port, service in ports_to_check:
        if check_public_access("178.104.109.237", port):
            print(f"端口 {port} ({service}): ✅ 公网访问正常")
        else:
            print(f"端口 {port} ({service}): ❌ 公网访问被阻止")
    
    print()
    print("=== 问题诊断 ===")
    
    # 检查可能的Docker配置
    docker_config_files = [
        "/proc/self/cgroup",
        "/.dockerenv"
    ]
    
    for file in docker_config_files:
        if os.path.exists(file):
            print(f"✅ 确认是Docker容器环境: {file}")
    
    print()
    print("=== 解决方案 ===")
    print()
    print("1. **检查Docker运行命令**:")
    print("   在宿主机上运行: docker ps --format 'table {{.Names}}\t{{.Ports}}'")
    print()
    print("2. **如果端口未映射，需要重新运行容器**:")
    print("   docker run -d \\")
    print("     -p 8082:8082 \\")
    print("     -p 5010:5010 \\")
    print("     -p 5020:5020 \\")
    print("     --name openclaw \\")
    print("     [镜像名称]")
    print()
    print("3. **或者添加端口映射到现有容器**:")
    print("   docker stop openclaw")
    print("   docker commit openclaw openclaw-backup")
    print("   docker run -d \\")
    print("     --name openclaw-new \\")
    print("     -p 8082:8082 \\")
    print("     -p 5010:5010 \\")
    print("     -p 5020:5020 \\")
    print("     openclaw-backup")
    print()
    print("4. **云服务商安全组配置**:")
    print("   即使端口映射正确，也需要在云服务商控制台配置安全组")
    print("   允许入站流量到端口: 8082, 5010, 5020")
    
    # 生成配置指令
    print()
    print("=== 配置指令总结 ===")
    print("1. Docker端口映射: -p 8082:8082 -p 5010:5010 -p 5020:5020")
    print("2. 云服务商安全组规则:")
    print("   - 端口8082: 允许所有IP (TCP)")
    print("   - 端口5010: 允许所有IP (TCP)")
    print("   - 端口5020: 允许所有IP (TCP)")
    print("3. 测试命令:")
    print("   curl http://178.104.109.237:8082/")
    print("   curl http://178.104.109.237:5010/")
    print("   curl http://178.104.109.237:5020/")

if __name__ == "__main__":
    main()