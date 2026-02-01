# API 文档

生成时间: 2026-02-01 00:08:11

## 端点列表

### /api/auth/login

#### POST /api/auth/login

用户登录 使用用户名和密码登录系统

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| body | object | body | 是 | JSON 请求体 |

**示例:**

```python
import requests

data = {}
response = requests.post('http://api.example.com/api/auth/login', json=data)
print(response.json())
```

---

### /api/posts

#### GET /api/posts

获取文章列表 返回所有文章信息，支持分页和搜索

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| page | string | query | 否 | 查询参数 page |
| limit | string | query | 否 | 查询参数 limit |
| keyword | string | query | 否 | 查询参数 keyword |

**示例:**

```python
import requests

response = requests.get('http://api.example.com/api/posts')
print(response.json())
```

---

### /api/users

#### GET /api/users

获取用户列表 返回所有用户的信息

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| page | string | query | 否 | 查询参数 page |
| limit | string | query | 否 | 查询参数 limit |

**示例:**

```python
import requests

response = requests.get('http://api.example.com/api/users')
print(response.json())
```

---

#### POST /api/users

创建新用户 提交用户信息创建新用户

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| body | object | body | 是 | JSON 请求体 |

**示例:**

```python
import requests

data = {}
response = requests.post('http://api.example.com/api/users', json=data)
print(response.json())
```

---

### /api/users/<int:user_id>

#### GET /api/users/<int:user_id>

获取单个用户信息 根据用户 ID 返回用户详细信息

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| user_id | int | path | 是 | 路径参数 user_id |

**示例:**

```python
import requests

response = requests.get('http://api.example.com/api/users/<int:user_id>')
print(response.json())
```

---

#### PUT /api/users/<int:user_id>

更新用户信息 根据用户 ID 更新用户信息

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| user_id | int | path | 是 | 路径参数 user_id |
| body | object | body | 是 | JSON 请求体 |

**示例:**

```python
import requests

data = {}
response = requests.put('http://api.example.com/api/users/<int:user_id>', json=data)
print(response.json())
```

---

#### DELETE /api/users/<int:user_id>

删除用户 根据用户 ID 删除用户

**参数:**

| 名称 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| user_id | int | path | 是 | 路径参数 user_id |
| page | string | query | 否 | 查询参数 page |
| limit | string | query | 否 | 查询参数 limit |
| keyword | string | query | 否 | 查询参数 keyword |

**示例:**

```python
import requests

response = requests.delete('http://api.example.com/api/users/<int:user_id>')
print(response.json())
```

---

