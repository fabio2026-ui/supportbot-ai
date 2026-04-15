#!/bin/bash
# ============================================
# Docker端口映射修复脚本 (宿主机执行)
# 解决AI游戏商店和支付系统外部访问问题
# ============================================

echo "🎯 Docker端口映射修复脚本"
echo "=========================="
echo "当前问题: 服务在容器内运行，但外部无法访问"
echo "解决方案: 重新创建容器并正确映射端口"
echo ""

# 1. 检查当前容器状态
echo "🔍 检查当前容器状态..."
docker ps -a | grep -E "openclaw|game|payment"

echo ""
echo "📊 当前端口映射状态:"
docker ps --format 'table {{.Names}}\t{{.Ports}}' | grep -E "openclaw|game|payment" || echo "未找到相关容器"

echo ""
echo "⚠️  如果看到类似 '0.0.0.0:8082->8082/tcp' 的映射，说明端口已正确映射"
echo "⚠️  如果只看到 '8082/tcp'，说明端口未映射到宿主机"

echo ""
read -p "是否继续修复? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 用户取消操作"
    exit 1
fi

# 2. 停止并删除旧容器
echo "🛑 停止并删除旧容器..."
docker stop openclaw 2>/dev/null || true
docker rm openclaw 2>/dev/null || true

# 3. 检查镜像是否存在
echo "🔍 检查Docker镜像..."
if ! docker images | grep -q "openclaw"; then
    echo "⚠️  未找到openclaw镜像，可能需要构建或拉取"
    echo "   请确保有openclaw:latest镜像"
    read -p "是否继续? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 4. 创建新容器并映射所有端口
echo "🚀 创建新容器并映射端口..."
docker run -d \
  --name openclaw \
  --restart unless-stopped \
  -p 8082:8082 \
  -p 5010:5010 \
  -p 5020:5020 \
  -v /home/node/.openclaw:/app/.openclaw \
  openclaw:latest

# 5. 等待容器启动
echo "⏳ 等待容器启动..."
sleep 5

# 6. 验证端口映射
echo "✅ 验证端口映射..."
echo ""
echo "📋 容器端口映射状态:"
docker port openclaw

echo ""
echo "📊 容器运行状态:"
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep openclaw

# 7. 测试服务访问
echo ""
echo "🧪 测试服务访问..."
echo "1. AI游戏商店 (端口8082):"
curl -s -o /dev/null -w "HTTP状态码: %{http_code}\n" http://localhost:8082/ || echo "访问失败"

echo ""
echo "2. 支付系统 (端口5010):"
curl -s -o /dev/null -w "HTTP状态码: %{http_code}\n" http://localhost:5010/ || echo "访问失败"

# 8. 获取外部IP
echo ""
echo "🌐 获取外部IP地址..."
EXTERNAL_IP=$(curl -s https://api.ipify.org)
echo "外部IP: $EXTERNAL_IP"

echo ""
echo "📝 访问地址:"
echo "AI游戏商店: http://$EXTERNAL_IP:8082"
echo "支付系统:   http://$EXTERNAL_IP:5010"

echo ""
echo "🎉 修复完成!"
echo ""
echo "🔧 如果外部仍然无法访问，请检查:"
echo "1. 云服务商安全组 (允许端口8082, 5010, 5020)"
echo "2. 宿主机防火墙: sudo ufw status"
echo "3. 网络配置"
echo ""
echo "📋 安全组配置指南已保存在 cloud_security_group_guide.md"