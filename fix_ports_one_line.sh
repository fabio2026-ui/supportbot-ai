#!/bin/bash
# 单行修复命令 (宿主机执行)
echo "复制以下命令在宿主机执行:"
echo ""
echo "# ============================================"
echo "# Docker端口映射修复 (单行命令)"
echo "# ============================================"
echo "docker stop openclaw 2>/dev/null || true; docker rm openclaw 2>/dev/null || true; docker run -d --name openclaw --restart unless-stopped -p 8082:8082 -p 5010:5010 -p 5020:5020 -v /home/node/.openclaw:/app/.openclaw openclaw:latest; sleep 3; echo '✅ 容器已启动'; docker ps --format 'table {{.Names}}\t{{.Ports}}' | grep openclaw; EXTERNAL_IP=\$(curl -s https://api.ipify.org); echo ''; echo '🌐 外部访问地址:'; echo 'AI游戏商店: http://'\$EXTERNAL_IP':8082'; echo '支付系统:   http://'\$EXTERNAL_IP':5010'"
echo ""
echo "# ============================================"
echo "# 验证命令"
echo "# ============================================"
echo "curl -I http://localhost:8082/"
echo "curl -I http://localhost:5010/"