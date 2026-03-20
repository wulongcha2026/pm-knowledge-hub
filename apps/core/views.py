from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Document, Category, Tag, SearchLog


def index(request):
    """首页 - 文档列表"""
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    
    documents = Document.objects.filter(is_public=True)
    
    # 搜索功能
    if query:
        documents = documents.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(summary__icontains=query)
        )
        # 记录搜索日志
        SearchLog.objects.create(
            query=query,
            results_count=documents.count(),
            ip_address=request.META.get('REMOTE_ADDR')
        )
    
    # 分类筛选
    if category_id:
        documents = documents.filter(category_id=category_id)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()[:10]
    
    context = {
        'documents': documents,
        'categories': categories,
        'tags': tags,
        'query': query,
    }
    return render(request, 'core/index.html', context)


def document_detail(request, pk):
    """文档详情"""
    document = get_object_or_404(Document, pk=pk, is_public=True)
    document.view_count += 1
    document.save()
    
    # 相关文档
    related = Document.objects.filter(
        category=document.category,
        is_public=True
    ).exclude(pk=document.pk)[:5]
    
    context = {
        'document': document,
        'related': related,
    }
    return render(request, 'core/document_detail.html', context)
