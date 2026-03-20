#!/bin/bash
# PM Knowledge Hub 快速初始化脚本

set -e

PROJECT_DIR="/root/.openclaw/workspace/projects/pm-knowledge-hub"
VENV_DIR="$PROJECT_DIR/venv"

echo "🍵 乌龙茶 PM Knowledge Hub 初始化脚本"
echo "======================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3"
    exit 1
fi

echo "✅ Python 版本：$(python3 --version)"
echo ""

# 进入项目目录
cd $PROJECT_DIR

# 1. 创建虚拟环境
echo "📦 步骤 1/5: 创建虚拟环境..."
python3 -m venv $VENV_DIR

# 2. 激活并安装依赖
echo "📥 步骤 2/5: 安装依赖（可能需要几分钟）..."
source $VENV_DIR/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

# 3. 数据库迁移
echo "🗄️  步骤 3/5: 数据库迁移..."
python manage.py makemigrations
python manage.py migrate

# 4. 创建超级用户提示
echo ""
echo "👤 步骤 4/5: 创建超级用户"
echo "请设置管理员账号密码："
python manage.py createsuperuser

# 5. 收集静态文件
echo "📁 步骤 5/5: 收集静态文件..."
python manage.py collectstatic --noinput

# 创建必要目录
mkdir -p media chroma_db

echo ""
echo "======================================"
echo "✅ 初始化完成！"
echo "======================================"
echo ""
echo "📌 启动开发服务器："
echo "   cd $PROJECT_DIR"
echo "   source $VENV_DIR/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8000"
echo ""
echo "🌐 访问地址："
echo "   http://localhost:8000"
echo "   http://test.pm.xyzliving.com (生产环境)"
echo ""
echo "📚 下一步："
echo "   1. 访问 /admin 登录后台"
echo "   2. 创建文档分类和标签"
echo "   3. 上传项目文档"
echo "   4. 运行导入脚本：python scripts/import_documents.py"
echo "   5. 开始使用 RAG 问答和风险识别功能！"
echo ""
