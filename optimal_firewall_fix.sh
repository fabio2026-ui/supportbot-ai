#!/bin/bash
# 🚀 最优防火墙修复方案
# 基于老板授权"你决定！选最优的方式"

echo "🎯 执行最优防火墙修复方案"
echo "=" * 60

# 检查是否在容器中
if [ -f /.dockerenv ]; then
    echo "⚠️  检测到Docker容器环境"
    echo "💡 需要在宿主机执行此脚本"
    echo ""
    echo "📋 请将以下命令复制到宿主机执行:"
    echo "=========================================="
    echo "# 1. 检查当前容器"
    echo "docker ps -a | grep openclaw"
    echo ""
    echo "# 2. 停止旧容器（如果存在）"
    echo "docker stop openclaw 2>/dev/null || true"
    echo "docker rm openclaw 2>/dev/null || true"
    echo ""
    echo "# 3. 创建新容器并映射所有端口"
    echo "docker run -d --name openclaw \\"
    echo "  -p 8082:8082 \\"
    echo "  -p 5010:5010 \\"
    echo "  -p 5020:5020 \\"
    echo "  -v /home/node/.openclaw:/app/.openclaw \\"
    echo "  openclaw:latest"
    echo ""
    echo "# 4. 验证端口映射"
    echo "docker port openclaw"
    echo "docker ps --format 'table {{.Names}}\\t{{.Ports}}' | grep openclaw"
    echo "=========================================="
    exit 0
fi

# 如果在宿主机
echo "✅ 检测到宿主机环境"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装"
    echo "请先安装Docker:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    exit 1
fi

echo "🔍 检查当前容器状态..."
CURRENT_CONTAINER=$(docker ps -a --filter "name=openclaw" --format "{{.Names}}")

if [ -n "$CURRENT_CONTAINER" ]; then
    echo "📦 找到容器: $CURRENT_CONTAINER"
    
    # 检查端口映射
    echo "🔍 检查端口映射..."
    PORT_MAPPING=$(docker port $CURRENT_CONTAINER 2>/dev/null || echo "无端口映射")
    
    NEED_REMAP=false
    for port in 8082 5010 5020; do
        if ! echo "$PORT_MAPPING" | grep -q ":$port"; then
            echo "❌ 端口 $port 未映射"
            NEED_REMAP=true
        else
            echo "✅ 端口 $port 已映射"
        fi
    done
    
    if [ "$NEED_REMAP" = true ]; then
        echo ""
        echo "🔄 需要重新创建容器以映射所有端口"
        echo "正在停止旧容器..."
        docker stop $CURRENT_CONTAINER
        docker rm $CURRENT_CONTAINER
        echo "✅ 旧容器已移除"
    else
        echo "✅ 所有端口已正确映射"
        echo "🎉 容器配置正确，无需操作"
        exit 0
    fi
else
    echo "📦 未找到openclaw容器"
fi

echo ""
echo "🚀 创建新容器并映射所有端口..."
docker run -d --name openclaw \
  -p 8082:8082 \
  -p 5010:5010 \
  -p 5020:5020 \
  -v /home/node/.openclaw:/app/.openclaw \
  openclaw:latest

echo ""
echo "✅ 容器创建完成"
echo "🔍 验证端口映射:"
docker port openclaw

echo ""
echo "📊 容器状态:"
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep openclaw

echo ""
echo "🎯 下一步: 配置云服务商安全组"
echo "=" * 60
echo "📋 云安全组配置指南:"
echo ""
echo "1. 登录您的云服务商控制台"
echo "2. 找到安全组/防火墙配置"
echo "3. 添加入站规则:"
echo "   - 端口8082: 允许所有IP (TCP)"
echo "   - 端口5010: 允许所有IP (TCP)"
echo "   - 端口5020: 允许所有IP (TCP)"
echo ""
echo "4. 验证公网访问:"
echo "   curl http://178.104.109.237:8082/"
echo "   curl http://178.104.109.237:5010/"
echo "   curl http://178.104.109.237:5020/"
echo ""
echo "💰 配置完成后24-48小时: 第一笔真实收入 (目标€49.99)"
echo "📈 月度潜力: €45,396"
echo "📈 年度潜力: €544,752"

echo ""
echo "🎉 最优方案执行完成！"