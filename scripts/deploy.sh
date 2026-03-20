#!/bin/bash
# PM Knowledge Hub 部署脚本

set -e

PROJECT_DIR="/root/.openclaw/workspace/projects/pm-knowledge-hub"
VENV_DIR="$PROJECT_DIR/venv"

echo "🍵 开始部署 PM Knowledge Hub..."

# 1. 创建虚拟环境
echo "📦 创建虚拟环境..."
cd $PROJECT_DIR
python3 -m venv $VENV_DIR

# 2. 激活虚拟环境并安装依赖
echo "📥 安装依赖..."
source $VENV_DIR/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. 数据库迁移
echo "🗄️ 数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 4. 收集静态文件
echo "📁 收集静态文件..."
python manage.py collectstatic --noinput

# 5. 创建必要的目录
echo "📂 创建目录..."
mkdir -p media chroma_db

# 6. 设置权限
echo "🔐 设置权限..."
chmod -R 755 $PROJECT_DIR

echo "✅ 部署完成！"
echo ""
echo "启动服务："
echo "  cd $PROJECT_DIR"
echo "  source $VENV_DIR/bin/activate"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "或使用 Gunicorn："
echo "  gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4"
