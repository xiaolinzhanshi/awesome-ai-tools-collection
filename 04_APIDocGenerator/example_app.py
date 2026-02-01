#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 Flask API - 用于测试文档生成器
"""

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/users', methods=['GET'])
def get_users():
    """
    获取用户列表
    返回所有用户的信息
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    users = [
        {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com'},
        {'id': 2, 'name': '李四', 'email': 'lisi@example.com'},
    ]
    
    return jsonify({
        'success': True,
        'data': users,
        'page': page,
        'limit': limit
    })


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    获取单个用户信息
    根据用户 ID 返回用户详细信息
    """
    user = {
        'id': user_id,
        'name': '张三',
        'email': 'zhangsan@example.com',
        'created_at': '2026-01-01'
    }
    
    return jsonify({
        'success': True,
        'data': user
    })


@app.route('/api/users', methods=['POST'])
def create_user():
    """
    创建新用户
    提交用户信息创建新用户
    """
    data = request.get_json()
    
    # 验证数据
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            'success': False,
            'error': '缺少必要字段'
        }), 400
    
    # 创建用户
    new_user = {
        'id': 3,
        'name': data['name'],
        'email': data['email'],
        'created_at': '2026-02-01'
    }
    
    return jsonify({
        'success': True,
        'data': new_user
    }), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    更新用户信息
    根据用户 ID 更新用户信息
    """
    data = request.get_json()
    
    updated_user = {
        'id': user_id,
        'name': data.get('name', '张三'),
        'email': data.get('email', 'zhangsan@example.com'),
        'updated_at': '2026-02-01'
    }
    
    return jsonify({
        'success': True,
        'data': updated_user
    })


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    删除用户
    根据用户 ID 删除用户
    """
    return jsonify({
        'success': True,
        'message': f'用户 {user_id} 已删除'
    })


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    获取文章列表
    返回所有文章信息，支持分页和搜索
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    keyword = request.args.get('keyword', '')
    
    posts = [
        {'id': 1, 'title': '第一篇文章', 'author': '张三'},
        {'id': 2, 'title': '第二篇文章', 'author': '李四'},
    ]
    
    return jsonify({
        'success': True,
        'data': posts,
        'page': page,
        'limit': limit
    })


@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    用户登录
    使用用户名和密码登录系统
    """
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')
    
    if username == 'admin' and password == 'password':
        return jsonify({
            'success': True,
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
            'user': {
                'id': 1,
                'username': 'admin',
                'role': 'admin'
            }
        })
    
    return jsonify({
        'success': False,
        'error': '用户名或密码错误'
    }), 401


if __name__ == '__main__':
    app.run(debug=True, port=5000)
