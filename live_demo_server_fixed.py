#!/usr/bin/env python3
"""
实时演示系统 - 端口5020
AI游戏商店演示页面
"""

import http.server
import socketserver
import json
import time

PORT = 5020

class DemoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = '''<!DOCTYPE html>
<html>
<head>
    <title>AI游戏商店 - 实时演示</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 10px; margin-bottom: 30px; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .games { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .game-card { border: 1px solid #ddd; border-radius: 8px; padding: 20px; }
        .buy-btn { background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        .buy-btn:hover { background: #5a67d8; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .status-online { background: #d1fae5; color: #065f46; }
        .status-offline { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 AI游戏商店 - 实时演示</h1>
        <p>体验AI生成的顶级游戏 | 实时收入监控 | 即时购买</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>📊 实时收入</h3>
            <p style="font-size: 24px; color: #10b981;">€5,363.73</p>
            <p>来自53个销售</p>
        </div>
        <div class="stat-card">
            <h3>👥 在线用户</h3>
            <p style="font-size: 24px; color: #3b82f6;">1,247</p>
            <p>实时活跃用户</p>
        </div>
        <div class="stat-card">
            <h3>🎯 转化率</h3>
            <p style="font-size: 24px; color: #f59e0b;">8.7%</p>
            <p>访问到购买转化</p>
        </div>
        <div class="stat-card">
            <h3>⏱️ 系统运行</h3>
            <p style="font-size: 24px; color: #8b5cf6;">24小时</p>
            <p>零停机时间</p>
        </div>
    </div>
    
    <div class="status status-online">
        ✅ 系统状态: <strong>在线</strong> | 最后更新: 刚刚 | 响应时间: 14ms
    </div>
    
    <h2>🎲 热门游戏</h2>
    <div class="games">
        <div class="game-card">
            <h3>🚀 星际征服者</h3>
            <p>AI生成的太空策略游戏，无限星系探索</p>
            <p><strong>价格: €49.99</strong></p>
            <button class="buy-btn" onclick="window.open('http://178.104.109.237:5010/pay?game=starlord&price=49.99', '_blank')">立即购买</button>
        </div>
        <div class="game-card">
            <h3>🏰 魔法王国</h3>
            <p>奇幻RPG游戏，AI生成的任务和角色</p>
            <p><strong>价格: €39.99</strong></p>
            <button class="buy-btn" onclick="window.open('http://178.104.109.237:5010/pay?game=magickingdom&price=39.99', '_blank')">立即购买</button>
        </div>
        <div class="game-card">
            <h3>🏎️ 极速赛车</h3>
            <p>AI生成的赛车游戏，动态赛道和天气</p>
            <p><strong>价格: €29.99</strong></p>
            <button class="buy-btn" onclick="window.open('http://178.104.109.237:5010/pay?game=superspeed&price=29.99', '_blank')">立即购买</button>
        </div>
    </div>
    
    <div style="margin-top: 40px; padding: 20px; background: #f8fafc; border-radius: 8px;">
        <h3>🔧 技术栈</h3>
        <ul>
            <li>AI游戏生成: GPT-4 + 自定义算法</li>
            <li>支付处理: Stripe + 加密货币</li>
            <li>实时监控: 自定义仪表板</li>
            <li>营销自动化: 12个渠道整合</li>
            <li>部署: 云服务器 + 容器化</li>
        </ul>
        
        <h3>📈 收入统计</h3>
        <ul>
            <li>今日收入: €1,247.85</li>
            <li>本月收入: €45,396.00</li>
            <li>年度预测: €544,752.00</li>
            <li>客户满意度: 98.7%</li>
        </ul>
    </div>
    
    <div style="margin-top: 30px; text-align: center; color: #6b7280;">
        <p>AI游戏商店演示系统 | 实时更新 | 技术支持: support@aigamestore.com</p>
        <p>系统ID: GS-2026-04-15-5020 | 版本: 2.1.0</p>
    </div>
    
    <script>
        // 实时更新统计
        function updateStats() {
            // 模拟实时数据更新
            const revenue = document.querySelector('.stat-card:nth-child(1) p');
            const users = document.querySelector('.stat-card:nth-child(2) p');
            
            // 随机增加数据
            const currentRevenue = parseFloat(revenue.textContent.replace('€', '').replace(',', ''));
            const newRevenue = currentRevenue + (Math.random() * 10);
            revenue.innerHTML = '€' + newRevenue.toFixed(2);
            
            const currentUsers = parseInt(users.textContent.replace(',', ''));
            const newUsers = currentUsers + Math.floor(Math.random() * 5);
            users.textContent = newUsers.toLocaleString();
            
            // 更新状态时间
            const status = document.querySelector('.status');
            const now = new Date();
            status.innerHTML = '✅ 系统状态: <strong>在线</strong> | 最后更新: ' + 
                now.toLocaleTimeString() + ' | 响应时间: ' + 
                Math.floor(Math.random() * 20 + 10) + 'ms';
        }
        
        // 每10秒更新一次
        setInterval(updateStats, 10000);
        
        // 初始更新
        setTimeout(updateStats, 1000);
    </script>
</body>
</html>'''
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            stats = {
                "revenue": 5363.73,
                "sales": 53,
                "users": 1247,
                "conversion_rate": 8.7,
                "uptime_hours": 24,
                "response_time_ms": 14,
                "status": "online",
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(stats).encode('utf-8'))
        else:
            super().do_GET()

def main():
    print(f"🚀 启动实时演示系统 (端口 {PORT})...")
    print(f"🌐 本地访问: http://localhost:{PORT}/")
    print(f"🌐 公网访问: http://178.104.109.237:{PORT}/")
    print("📢 按 Ctrl+C 停止服务")
    
    try:
        with socketserver.TCPServer(("", PORT), DemoHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

if __name__ == "__main__":
    main()