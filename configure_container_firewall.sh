#!/bin/bash
# 容器防火墙配置脚本
# 用于在Docker容器中配置端口转发和访问控制

echo "=== 容器防火墙配置 ==="
echo "公网IP: 178.104.109.237"
echo "需要开放的端口: 8082, 5010, 5020"

# 检查当前监听的端口
echo ""
echo "=== 当前监听的端口 ==="
python3 -c "
import socket
import sys

ports = [8082, 5010, 5020]
for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex(('0.0.0.0', port))
    if result == 0:
        print(f'端口 {port}: ✅ 正在监听')
    else:
        print(f'端口 {port}: ❌ 未监听')
    sock.close()
"

# 检查服务状态
echo ""
echo "=== 服务状态检查 ==="
echo "1. AI游戏商店 (端口8082):"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8082/ 2>/dev/null && echo " ✅ 运行正常" || echo " ❌ 未运行"

echo ""
echo "2. 支付系统 (端口5010):"
curl -s -o /dev/null -w "%{http_code}" http://localhost:5010/ 2>/dev/null && echo " ✅ 运行正常" || echo " ❌ 未运行"

echo ""
echo "=== 配置建议 ==="
echo ""
echo "由于这是Docker容器环境，防火墙配置需要在宿主机或云服务商层面进行："
echo ""
echo "1. **Docker运行命令** (如果容器重启):"
echo "   docker run -p 8082:8082 -p 5010:5010 -p 5020:5020 [其他参数]"
echo ""
echo "2. **云服务商安全组配置** (如果使用VPS):"
echo "   - 登录云服务商控制台"
echo "   - 找到安全组/防火墙规则"
echo "   - 添加以下入站规则:"
echo "     * 端口8082: 允许所有IP (TCP)"
echo "     * 端口5010: 允许所有IP (TCP)"  
echo "     * 端口5020: 允许所有IP (TCP)"
echo ""
echo "3. **测试公网访问**:"
echo "   curl http://178.104.109.237:8082/"
echo "   curl http://178.104.109.237:5010/"
echo ""
echo "=== 当前容器网络信息 ==="
hostname -I 2>/dev/null || echo "无法获取IP信息"

echo ""
echo "=== 下一步行动 ==="
echo "1. 检查容器是否已正确映射端口到宿主机"
echo "2. 配置宿主机或云服务商防火墙"
echo "3. 验证公网访问"