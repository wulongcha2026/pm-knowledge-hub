# PM Knowledge Hub - 项目管理知识库

基于 Django 6 + LangChain + Chroma 的项目管理知识库系统。

## 功能模块

### 1. 基础知识库（无需登录）
- 文档上传与管理
- 关键字搜索
- 分类/标签管理
- 公开浏览

### 2. PM 知识问答助手（需登录）
- 基于 RAG 的智能问答
- 支持上传项目文档作为知识库
- 对话历史记录
- 引用来源展示
- 技术栈：LangChain + Chroma + bge-m3

### 3. 项目风险识别 Agent（需登录）
- 输入项目描述或会议纪要
- 输出风险清单和应对建议
- 基于 LangGraph 多步推理
- 风险等级评估

## 技术栈

- **后端框架**: Django 6 + Django REST Framework
- **数据库**: SQLite
- **向量数据库**: Chroma
- **AI 框架**: LangChain + LangGraph
- **嵌入模型**: bge-m3（本地运行，免费）
- **LLM**: 智谱 GLM-4.7（OpenAI 兼容接口）
- **前端**: Django Templates + Tailwind CSS

## 快速开始

### 1. 安装依赖

```bash
cd /root/.openclaw/workspace/projects/pm-knowledge-hub
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件：

```bash
# 智谱 AI 配置
ZHIPU_API_KEY=your_api_key
ZHIPU_API_BASE=https://open.bigmodel.cn/api/coding/paas/v4
ZHIPU_LLM_MODEL=glm-4-flash

# 嵌入模型配置
EMBEDDING_MODEL=bge-m3
EMBEDDING_DEVICE=cpu
```

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户

```bash
python manage.py createsuperuser
```

### 5. 运行开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

访问：http://localhost:8000

## 部署到生产环境

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name test.pm.xyzliving.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /root/.openclaw/workspace/projects/pm-knowledge-hub/staticfiles/;
    }

    location /media/ {
        alias /root/.openclaw/workspace/projects/pm-knowledge-hub/media/;
    }
}
```

### 使用 Gunicorn 运行

```bash
gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4
```

## 项目结构

```
pm-knowledge-hub/
├── manage.py
├── requirements.txt
├── .env
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/          # 基础知识库
│   ├── accounts/      # 用户认证
│   ├── rag/           # RAG 问答助手
│   └── risk_agent/    # 风险识别 Agent
├── static/
├── media/
└── scripts/
```

## API 文档

### RAG 聊天 API

```bash
POST /rag/api/chat/
Content-Type: application/json
Authorization: Session <session_id>

{
    "question": "什么是项目风险管理？",
    "conversation_id": 1  # 可选，继续之前的对话
}
```

### 风险分析 API

```bash
POST /risk/api/analyze/
Content-Type: application/json
Authorization: Session <session_id>

{
    "title": "XX 项目风险评估",
    "project_description": "项目描述...",
    "meeting_notes": "会议纪要..."
}
```

## 开发计划

- [x] 项目框架搭建
- [x] 用户认证系统
- [x] 基础知识库
- [x] RAG 服务集成
- [x] 风险识别 Agent
- [ ] 前端模板完善
- [ ] 文档导入脚本
- [ ] 性能优化
- [ ] SSL 证书配置

## License

MIT

## 作者

Winfred & 乌龙茶 🍵
