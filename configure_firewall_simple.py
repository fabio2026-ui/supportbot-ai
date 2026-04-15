#!/usr/bin/env python3
"""
简单防火墙配置脚本
用于配置云服务商安全组/防火墙规则
"""

import os
import sys
import subprocess
import json

def check_current_firewall():
    """检查当前防火墙状态"""
    print("🔍 检查当前防火墙状态...")
    
    # 检查iptables规则
    try:
        result = subprocess.run(['sudo', 'iptables', '-L', '-n'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ iptables 可访问")
            # 检查是否有相关端口规则
            for port in [8082, 5010, 5020]:
                if f":{port}" in result.stdout:
                    print(f"✅ 端口 {port} 已在规则中")
                else:
                    print(f"❌ 端口 {port} 未在规则中")
        else:
            print("⚠️  iptables 检查失败 (可能需要sudo权限)")
    except Exception as e:
        print(f"⚠️  iptables 检查异常: {e}")
    
    # 检查ufw状态
    try:
        result = subprocess.run(['sudo', 'ufw', 'status'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("UFW状态:")
            print(result.stdout)
    except Exception as e:
        print(f"UFW检查异常: {e}")

def create_firewall_config():
    """创建防火墙配置文件"""
    config = {
        "public_ip": "178.104.109.237",
        "ports_to_open": [
            {"port": 8082, "service": "AI游戏商店", "protocol": "tcp"},
            {"port": 5010, "service": "支付系统", "protocol": "tcp"},
            {"port": 5020, "service": "实时演示系统", "protocol": "tcp"},
            {"port": 80, "service": "HTTP", "protocol": "tcp"},
            {"port": 443, "service": "HTTPS", "protocol": "tcp"}
        ],
        "security_group_rules": [
            "允许所有IP访问端口8082 (游戏商店)",
            "允许所有IP访问端口5010 (支付系统)",
            "允许所有IP访问端口5020 (演示系统)",
            "限制SSH端口22仅允许特定IP",
            "启用DDoS防护"
        ]
    }
    
    config_path = "/home/node/.openclaw/workspace/firewall_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 防火墙配置已保存到: {config_path}")
    return config

def generate_cloud_provider_commands():
    """生成云服务商命令"""
    print("\n🌐 云服务商安全组配置命令:")
    print("=" * 60)
    
    providers = {
        "AWS EC2": [
            "# 1. 进入EC2控制台 -> 安全组",
            "# 2. 编辑入站规则:",
            "aws ec2 authorize-security-group-ingress \\",
            "  --group-id YOUR-SG-ID \\",
            "  --protocol tcp \\",
            "  --port 8082 \\",
            "  --cidr 0.0.0.0/0",
            "",
            "aws ec2 authorize-security-group-ingress \\",
            "  --group-id YOUR-SG-ID \\",
            "  --protocol tcp \\",
            "  --port 5010 \\",
            "  --cidr 0.0.0.0/0",
            "",
            "aws ec2 authorize-security-group-ingress \\",
            "  --group-id YOUR-SG-ID \\",
            "  --protocol tcp \\",
            "  --port 5020 \\",
            "  --cidr 0.0.0.0/0"
        ],
        "Google Cloud": [
            "# 1. 进入VPC网络 -> 防火墙规则",
            "# 2. 创建新规则:",
            "gcloud compute firewall-rules create allow-game-store \\",
            "  --allow tcp:8082 \\",
            "  --source-ranges 0.0.0.0/0",
            "",
            "gcloud compute firewall-rules create allow-payment \\",
            "  --allow tcp:5010 \\",
            "  --source-ranges 0.0.0.0/0",
            "",
            "gcloud compute firewall-rules create allow-demo \\",
            "  --allow tcp:5020 \\",
            "  --source-ranges 0.0.0.0/0"
        ],
        "DigitalOcean": [
            "# 1. 进入Networking -> Firewalls",
            "# 2. 添加入站规则:",
            "doctl compute firewall add-rules YOUR-FW-ID \\",
            "  --inbound-rules 'protocol:tcp,ports:8082,address:0.0.0.0/0'",
            "",
            "doctl compute firewall add-rules YOUR-FW-ID \\",
            "  --inbound-rules 'protocol:tcp,ports:5010,address:0.0.0.0/0'",
            "",
            "doctl compute firewall add-rules YOUR-FW-ID \\",
            "  --inbound-rules 'protocol:tcp,ports:5020,address:0.0.0.0/0'"
        ],
        "Linode": [
            "# 1. 进入Firewalls",
            "# 2. 添加规则:",
            "linode-cli firewalls rules-create \\",
            "  --id YOUR-FW-ID \\",
            "  --protocol TCP \\",
            "  --ports 8082 \\",
            "  --action ACCEPT \\",
            "  --addresses 0.0.0.0/0",
            "",
            "linode-cli firewalls rules-create \\",
            "  --id YOUR-FW-ID \\",
            "  --protocol TCP \\",
            "  --ports 5010 \\",
            "  --action ACCEPT \\",
            "  --addresses 0.0.0.0/0",
            "",
            "linode-cli firewalls rules-create \\",
            "  --id YOUR-FW-ID \\",
            "  --protocol TCP \\",
            "  --ports 5020 \\",
            "  --action ACCEPT \\",
            "  --addresses 0.0.0.0/0"
        ]
    }
    
    for provider, commands in providers.items():
        print(f"\n📋 {provider}:")
        print("-" * 40)
        for cmd in commands:
            print(cmd)
    
    print("\n" + "=" * 60)
    print("💡 提示: 请根据您的云服务商执行相应命令")
    print("      或联系云服务商客服协助配置安全组")

def create_local_firewall_script():
    """创建本地防火墙配置脚本（如果可能）"""
    script = """#!/bin/bash
# 本地防火墙配置脚本
# 注意：需要sudo权限执行

echo "🔧 配置本地防火墙规则..."

# 检查是否在容器中
if [ -f /.dockerenv ]; then
    echo "⚠️  检测到容器环境，防火墙配置可能受限"
    echo "💡 需要在宿主机或云服务商控制台配置安全组"
    exit 0
fi

# 检查iptables是否可用
if command -v iptables &> /dev/null; then
    echo "✅ iptables 可用"
    
    # 添加端口规则
    for port in 8082 5010 5020; do
        echo "添加端口 $port 规则..."
        sudo iptables -A INPUT -p tcp --dport $port -j ACCEPT
    done
    
    # 保存规则
    sudo iptables-save > /etc/iptables/rules.v4
    echo "✅ 防火墙规则已保存"
else
    echo "❌ iptables 不可用"
fi

# 检查ufw
if command -v ufw &> /dev/null; then
    echo "✅ UFW 可用"
    sudo ufw allow 8082/tcp
    sudo ufw allow 5010/tcp
    sudo ufw allow 5020/tcp
    echo "✅ UFW 规则已添加"
fi

echo "🎉 防火墙配置完成！"
echo "📢 注意：云服务商安全组仍需单独配置"
"""
    
    script_path = "/home/node/.openclaw/workspace/configure_firewall.sh"
    with open(script_path, 'w') as f:
        f.write(script)
    
    # 设置执行权限
    os.chmod(script_path, 0o755)
    print(f"✅ 本地防火墙脚本已创建: {script_path}")
    print(f"💡 执行命令: sudo bash {script_path}")

def main():
    print("🚀 防火墙配置助手")
    print("=" * 60)
    
    # 1. 检查当前状态
    check_current_firewall()
    
    # 2. 创建配置
    config = create_firewall_config()
    
    # 3. 生成云服务商命令
    generate_cloud_provider_commands()
    
    # 4. 创建本地脚本
    create_local_firewall_script()
    
    print("\n" + "=" * 60)
    print("🎯 下一步行动:")
    print("1. 根据您的云服务商执行安全组配置命令")
    print("2. 或联系云服务商客服协助配置")
    print("3. 配置完成后测试公网访问:")
    print("   http://178.104.109.237:8082/")
    print("   http://178.104.109.237:5010/")
    print("   http://178.104.109.237:5020/")
    print("4. 开始真实营销获取第一笔收入！")

if __name__ == "__main__":
    main()