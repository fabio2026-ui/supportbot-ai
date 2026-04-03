#!/usr/bin/env python3
"""
加密货币支付验证脚本
用于验证比特币和以太坊支付
"""

import json
import requests
from datetime import datetime

# 加密货币地址配置
CRYPTO_ADDRESSES = {
    "bitcoin": "bc1qnay69verr63h74tc8h3tvpg7gvjpktj336gmsf",
    "ethereum": "0xd43b2D60B0b03cEcce6f71dDF765648dA511dAa98"
}

# 区块链浏览器API端点
BLOCKCHAIN_APIS = {
    "bitcoin": "https://blockchain.info",
    "ethereum": "https://api.etherscan.io/api"
}

def verify_bitcoin_transaction(tx_hash):
    """
    验证比特币交易
    """
    try:
        url = f"{BLOCKCHAIN_APIS['bitcoin']}/rawtx/{tx_hash}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 检查交易是否确认
            confirmations = data.get('block_height', 0)
            if confirmations > 0:
                # 检查是否发送到我们的地址
                for output in data.get('out', []):
                    if output.get('addr') == CRYPTO_ADDRESSES['bitcoin']:
                        amount_btc = output.get('value', 0) / 100000000  # 转换为BTC
                        return {
                            "verified": True,
                            "confirmations": confirmations,
                            "amount_btc": amount_btc,
                            "timestamp": data.get('time', 0),
                            "tx_hash": tx_hash
                        }
            
            return {
                "verified": False,
                "confirmations": confirmations,
                "message": "交易未确认或未发送到指定地址"
            }
            
    except Exception as e:
        return {
            "verified": False,
            "error": str(e),
            "message": "验证失败"
        }

def verify_ethereum_transaction(tx_hash, api_key=""):
    """
    验证以太坊交易
    """
    try:
        # 如果没有API密钥，使用公共端点（有限制）
        if not api_key:
            url = f"{BLOCKCHAIN_APIS['ethereum']}?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey=YourApiKeyToken"
        else:
            url = f"{BLOCKCHAIN_APIS['ethereum']}?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={api_key}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('result'):
                tx_data = data['result']
                
                # 检查是否发送到我们的地址
                if tx_data.get('to', '').lower() == CRYPTO_ADDRESSES['ethereum'].lower():
                    # 获取交易确认数
                    receipt_url = f"{BLOCKCHAIN_APIS['ethereum']}?module=proxy&action=eth_getTransactionReceipt&txhash={tx_hash}&apikey={api_key if api_key else 'YourApiKeyToken'}"
                    receipt_response = requests.get(receipt_url, timeout=10)
                    
                    if receipt_response.status_code == 200:
                        receipt_data = receipt_response.json()
                        
                        if receipt_data.get('result'):
                            block_number = int(receipt_data['result'].get('blockNumber', '0x0'), 16)
                            
                            # 获取当前区块高度
                            block_url = f"{BLOCKCHAIN_APIS['ethereum']}?module=proxy&action=eth_blockNumber&apikey={api_key if api_key else 'YourApiKeyToken'}"
                            block_response = requests.get(block_url, timeout=10)
                            
                            if block_response.status_code == 200:
                                block_data = block_response.json()
                                current_block = int(block_data.get('result', '0x0'), 16)
                                confirmations = current_block - block_number if current_block > block_number else 0
                                
                                # 转换金额（wei 到 ETH）
                                amount_wei = int(tx_data.get('value', '0x0'), 16)
                                amount_eth = amount_wei / 10**18
                                
                                return {
                                    "verified": True,
                                    "confirmations": confirmations,
                                    "amount_eth": amount_eth,
                                    "block_number": block_number,
                                    "tx_hash": tx_hash
                                }
            
            return {
                "verified": False,
                "message": "交易未找到或未发送到指定地址"
            }
            
    except Exception as e:
        return {
            "verified": False,
            "error": str(e),
            "message": "验证失败"
        }

def check_address_balance(crypto_type):
    """
    检查地址余额（需要API密钥）
    """
    try:
        if crypto_type == "bitcoin":
            url = f"{BLOCKCHAIN_APIS['bitcoin']}/rawaddr/{CRYPTO_ADDRESSES['bitcoin']}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                balance_btc = data.get('final_balance', 0) / 100000000
                total_received_btc = data.get('total_received', 0) / 100000000
                
                return {
                    "balance_btc": balance_btc,
                    "total_received_btc": total_received_btc,
                    "transaction_count": data.get('n_tx', 0)
                }
                
        elif crypto_type == "ethereum":
            # 以太坊需要API密钥
            return {
                "message": "以太坊余额检查需要API密钥",
                "address": CRYPTO_ADDRESSES['ethereum']
            }
            
    except Exception as e:
        return {
            "error": str(e),
            "message": "余额检查失败"
        }

def generate_payment_report():
    """
    生成支付报告
    """
    report = {
        "timestamp": datetime.now().isoformat(),
        "addresses": CRYPTO_ADDRESSES,
        "status": "active",
        "instructions": {
            "bitcoin": "发送 $19.99 等值的比特币到上述地址",
            "ethereum": "发送 $19.99 等值的以太坊到上述地址"
        }
    }
    
    return report

def main():
    """主函数"""
    print("=" * 60)
    print("加密货币支付验证系统")
    print("=" * 60)
    
    print("\n📋 配置的加密货币地址：")
    print(f"比特币: {CRYPTO_ADDRESSES['bitcoin']}")
    print(f"以太坊: {CRYPTO_ADDRESSES['ethereum']}")
    
    print("\n🎯 使用说明：")
    print("1. 客户向上述地址发送加密货币")
    print("2. 客户提供交易哈希(TX Hash)")
    print("3. 使用此脚本验证交易")
    print("4. 确认后激活客户账户")
    
    print("\n🔧 可用功能：")
    print("1. 验证比特币交易")
    print("2. 验证以太坊交易")
    print("3. 检查地址余额")
    print("4. 生成支付报告")
    
    while True:
        print("\n" + "=" * 60)
        choice = input("\n请选择功能 (1-4, q退出): ").strip()
        
        if choice == '1':
            tx_hash = input("请输入比特币交易哈希: ").strip()
            result = verify_bitcoin_transaction(tx_hash)
            print("\n验证结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == '2':
            tx_hash = input("请输入以太坊交易哈希: ").strip()
            api_key = input("请输入Etherscan API密钥(可选): ").strip()
            result = verify_ethereum_transaction(tx_hash, api_key)
            print("\n验证结果:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == '3':
            crypto_type = input("请选择加密货币 (bitcoin/ethereum): ").strip().lower()
            result = check_address_balance(crypto_type)
            print("\n余额信息:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == '4':
            report = generate_payment_report()
            print("\n支付报告:")
            print(json.dumps(report, indent=2, ensure_ascii=False))
            
            # 保存报告到文件
            filename = f"crypto_payment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"\n✅ 报告已保存到: {filename}")
            
        elif choice.lower() == 'q':
            print("\n👋 感谢使用加密货币支付验证系统！")
            break
            
        else:
            print("❌ 无效选择，请重试")

if __name__ == "__main__":
    main()