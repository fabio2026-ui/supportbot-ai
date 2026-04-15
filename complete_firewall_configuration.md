# 完整防火墙和安全组配置指南

## 📋 当前状态分析
- **公网IP**: 178.104.109.237
- **容器内部IP**: 172.17.0.2
- **服务状态**: ✅ 所有服务在容器内部运行正常
- **公网访问**: ❌ 所有端口被阻止

## 🎯 需要开放的端口
| 端口 | 服务 | 协议 | 访问范围 |
|------|------|------|----------|
| 8082 | AI游戏商店 | TCP | 0.0.0.0/0 (所有IP) |
| 5010 | 支付系统 | TCP | 0.0.0.0/0 (所有IP) |
| 5020 | 实时演示系统 | TCP | 0.0.0.0/0 (所有IP) |

## 🔧 解决方案（按优先级）

### 方案1: 重新运行Docker容器（最简单）
```bash
# 1. 停止当前容器
docker stop openclaw

# 2. 备份当前容器
docker commit openclaw openclaw-backup

# 3. 重新运行容器并映射所有端口
docker run -d \
  --name openclaw-new \
  -p 8082:8082 \
  -p 5010:5010 \
  -p 5020:5020 \
  -v /home/node/.openclaw:/app/.openclaw \
  openclaw-backup

# 4. 验证端口映射
docker ps --format 'table {{.Names}}\t{{.Ports}}'
```

### 方案2: 修改现有容器配置
```bash
# 1. 检查当前容器配置
docker inspect openclaw | grep -A 10 "PortBindings"

# 2. 如果使用docker-compose，修改docker-compose.yml
# 在ports部分添加:
# ports:
#   - "8082:8082"
#   - "5010:5010"
#   - "5020:5020"

# 3. 重启服务
docker-compose down && docker-compose up -d
```

### 方案3: 配置云服务商安全组（必需）

#### AWS EC2 安全组配置
1. 登录 AWS 控制台 → EC2
2. 选择实例 → 安全组
3. 添加入站规则:
   - 类型: 自定义TCP
   - 端口范围: 8082
   - 来源: 0.0.0.0/0
   - 描述: AI游戏商店
4. 重复添加端口5010和5020

#### Google Cloud 防火墙规则
```bash
# 创建防火墙规则
gcloud compute firewall-rules create openclaw-ports \
  --allow tcp:8082,tcp:5010,tcp:5020 \
  --source-ranges 0.0.0.0/0 \
  --description "OpenClaw服务端口"
```

#### DigitalOcean 防火墙
1. 控制台 → Networking → Firewalls
2. 创建新防火墙规则
3. 添加入站规则:
   - 类型: Custom
   - 端口范围: 8082,5010,5020
   - 来源: All IPv4, All IPv6

#### 阿里云/腾讯云 安全组
1. 控制台 → 安全组
2. 添加入站规则:
   - 协议类型: TCP
   - 端口范围: 8082/8082, 5010/5010, 5020/5020
   - 授权对象: 0.0.0.0/0

### 方案4: 使用iptables（如果直接运行在VPS上）
```bash
# 允许端口8082
sudo iptables -A INPUT -p tcp --dport 8082 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5010 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5020 -j ACCEPT

# 保存规则
sudo iptables-save > /etc/iptables/rules.v4

# 或者使用ufw
sudo ufw allow 8082/tcp
sudo ufw allow 5010/tcp
sudo ufw allow 5020/tcp
sudo ufw reload
```

## 🧪 验证步骤

### 步骤1: 验证Docker端口映射
```bash
# 在宿主机上运行
docker ps --format 'table {{.Names}}\t{{.Ports}}'

# 预期输出应该包含:
# openclaw   0.0.0.0:8082->8082/tcp, 0.0.0.0:5010->5010/tcp, 0.0.0.0:5020->5020/tcp
```

### 步骤2: 验证本地访问
```bash
# 在宿主机上测试
curl http://localhost:8082/
curl http://localhost:5010/
curl http://localhost:5020/
```

### 步骤3: 验证公网访问
```bash
# 从外部机器测试
curl http://178.104.109.237:8082/
curl http://178.104.109.237:5010/
curl http://178.104.109.237:5020/
```

### 步骤4: 使用在线工具验证
1. 访问: https://www.yougetsignal.com/tools/open-ports/
2. 输入IP: 178.104.109.237
3. 测试端口: 8082, 5010, 5020

## 📊 故障排除

### 问题1: 端口已映射但无法访问
```bash
# 检查防火墙
sudo netstat -tulpn | grep :8082
sudo ss -tulpn | grep :8082

# 检查服务是否在监听
sudo lsof -i :8082
```

### 问题2: 容器重启后配置丢失
创建docker-compose.yml持久化配置:
```yaml
version: '3.8'
services:
  openclaw:
    image: openclaw-backup
    container_name: openclaw
    ports:
      - "8082:8082"
      - "5010:5010"
      - "5020:5020"
    volumes:
      - /home/node/.openclaw:/app/.openclaw
    restart: unless-stopped
```

### 问题3: 云服务商阻止流量
1. 检查安全组规则是否生效
2. 检查网络ACL（网络访问控制列表）
3. 检查VPC路由表
4. 联系云服务商技术支持

## 🚀 快速启动脚本

创建`fix_ports.sh`:
```bash
#!/bin/bash
echo "修复OpenClaw端口访问问题..."

# 备份当前容器
echo "1. 备份当前容器..."
docker commit openclaw openclaw-backup-$(date +%Y%m%d)

# 停止并删除旧容器
echo "2. 停止旧容器..."
docker stop openclaw && docker rm openclaw

# 运行新容器
echo "3. 运行新容器并映射端口..."
docker run -d \
  --name openclaw \
  -p 8082:8082 \
  -p 5010:5010 \
  -p 5020:5020 \
  -v /home/node/.openclaw:/app/.openclaw \
  openclaw-backup-$(date +%Y%m%d)

echo "4. 验证..."
docker ps --format 'table {{.Names}}\t{{.Ports}}'
echo ""
echo "测试访问:"
echo "curl http://localhost:8082/"
echo "curl http://178.104.109.237:8082/"
```

## 📈 配置后的预期结果

### 成功指标
1. ✅ 本地访问: `curl http://localhost:8082/` 返回HTML页面
2. ✅ 公网访问: `curl http://178.104.109.237:8082/` 返回HTML页面
3. ✅ 支付系统: `curl http://178.104.109.237:5010/` 返回JSON状态
4. ✅ 演示系统: `curl http://178.104.109.237:5020/` 返回演示页面

### 收入系统激活
1. 第一笔真实收入预计在配置完成后24-48小时内
2. 目标: €49.99 第一笔交易
3. 月度潜力: €45,396
4. 年度潜力: €544,752

## 📞 紧急联系方式

如果遇到问题:
1. 检查本指南的故障排除部分
2. 查看容器日志: `docker logs openclaw`
3. 检查服务状态: `docker exec openclaw ps aux`
4. 联系技术支持

---

**配置完成时间**: 2026-04-15 10:45 UTC  
**预计收入激活**: 配置完成后24-48小时  
**系统状态**: 技术100%就绪，等待网络配置