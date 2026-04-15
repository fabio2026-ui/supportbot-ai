#!/usr/bin/env python3
"""
Simple payment endpoint for testing
"""

from flask import Flask, request, jsonify
import stripe
import os
from dotenv import load_dotenv

# Load environment
load_dotenv('/home/node/.openclaw/workspace/.env')

app = Flask(__name__)

# Configure Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.json
        price_id = data.get('priceId')
        
        if not price_id:
            return jsonify({'error': 'Price ID required'}), 400
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=data.get('successUrl', 'https://example.com/success'),
            cancel_url=data.get('cancelUrl', 'https://example.com/cancel'),
        )
        
        return jsonify({
            'id': session.id,
            'url': session.url,
            'status': 'created'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'stripe': 'connected' if stripe.api_key else 'disconnected',
        'mode': 'live' if 'sk_live_' in str(stripe.api_key) else 'test'
    })

if __name__ == '__main__':
    print("Starting payment endpoint on port 5002...")
    print(f"Stripe mode: {'LIVE' if 'sk_live_' in str(stripe.api_key) else 'TEST'}")
    app.run(host='0.0.0.0', port=5002, debug=True)