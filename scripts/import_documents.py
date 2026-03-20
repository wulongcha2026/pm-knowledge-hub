#!/usr/bin/env python
"""
文档导入脚本 - 将文档导入到向量数据库
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Document
from apps.rag.services import get_rag_service


def import_documents():
    """导入文档到向量数据库"""
    print("🍵 开始导入文档到向量数据库...")
    
    # 获取所有公开文档
    documents = Document.objects.filter(is_public=True)
    
    if not documents:
        print("⚠️  没有找到公开文档，请先创建文档。")
        return
    
    rag_service = get_rag_service()
    
    # 准备文档数据
    docs_to_add = []
    for doc in documents:
        # 简单分块（实际项目中应该用更智能的分块策略）
        chunks = doc.content.split('\n\n')
        
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) > 50:  # 过滤太短的片段
                docs_to_add.append({
                    'id': f"{doc.id}_{i}",
                    'title': doc.title,
                    'content': chunk,
                    'source': f'document_{doc.id}',
                })
    
    if docs_to_add:
        print(f"📚 导入 {len(docs_to_add)} 个文档片段...")
        rag_service.add_documents(docs_to_add)
        print("✅ 导入完成！")
    else:
        print("⚠️  没有可导入的文档内容。")


if __name__ == '__main__':
    import_documents()
