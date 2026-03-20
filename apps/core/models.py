from django.db import models
from django.utils import timezone


class Category(models.Model):
    """文档分类"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='描述')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='父分类')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名称')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
    
    def __str__(self):
        return self.name


class Document(models.Model):
    """文档"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    summary = models.TextField(blank=True, verbose_name='摘要')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    file = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name='附件')
    is_public = models.BooleanField(default=True, verbose_name='公开')
    view_count = models.IntegerField(default=0, verbose_name='浏览次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '文档'
        verbose_name_plural = '文档'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.title


class SearchLog(models.Model):
    """搜索日志"""
    query = models.CharField(max_length=200, verbose_name='搜索关键词')
    results_count = models.IntegerField(default=0, verbose_name='结果数量')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP 地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='搜索时间')
    
    class Meta:
        verbose_name = '搜索日志'
        verbose_name_plural = '搜索日志'
        ordering = ['-created_at']
