import os
import http.server
import socketserver
from http import HTTPStatus

class GameStoreHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 设置默认页面
        if self.path == '/':
            self.path = '/public_game_store_stripe.html'
        elif self.path == '/stripe':
            self.path = '/public_game_store_stripe.html'
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def end_headers(self):
        # 添加CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        http.server.SimpleHTTPRequestHandler.end_headers(self)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == '__main__':
    PORT = 8082
    
    # 创建下载目录
    downloads_dir = 'downloads'
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        print(f'📁 创建下载目录: {downloads_dir}')
    
    # 创建一些示例游戏文件
    games = ['时空谜题', 'AI冒险岛', '量子迷宫', '未来城市建造者', '星际贸易大亨', '魔法学院模拟器']
    for game in games:
        zip_file = f'{downloads_dir}/{game}.zip'
        if not os.path.exists(zip_file):
            with open(zip_file, 'w') as f:
                f.write(f'# {game} 游戏文件\n\n这是一个高质量AI生成的游戏。\n解压后运行install.bat或install.sh开始游戏。\n\n')
            print(f'📦 创建游戏文件: {zip_file}')
    
    with socketserver.TCPServer(("0.0.0.0", PORT), GameStoreHandler) as httpd:
        print(f'🚀 游戏商店服务器启动中...')
        print(f'📡 公网地址: http://178.104.109.237:{PORT}')
        print(f'💳 Stripe商店: http://178.104.109.237:{PORT}/public_game_store_stripe.html')
        print(f'📁 下载目录: http://178.104.109.237:{PORT}/downloads/')
        print(f'🎮 可用游戏: {len(games)}款')
        print('🔄 按 Ctrl+C 停止服务器')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n🛑 服务器已停止')