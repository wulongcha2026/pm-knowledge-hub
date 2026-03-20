from django.db import models
from django.contrib.auth.models import User


class VectorDocument(models.Model):
    """向量文档 - 用于 RAG 检索"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    chunk_index = models.IntegerField(default=0, verbose_name='分块索引')
    embedding = models.JSONField(null=True, blank=True, verbose_name='向量嵌入')
    source_document = models.ForeignKey('core.Document', on_delete=models.CASCADE, verbose_name='来源文档')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '向量文档'
        verbose_name_plural = '向量文档'
        indexes = [
            models.Index(fields=['source_document']),
        ]


class Conversation(models.Model):
    """对话会话"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=200, blank=True, verbose_name='对话标题')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '对话'
        verbose_name_plural = '对话'
        ordering = ['-updated_at']


class Message(models.Model):
    """对话消息"""
    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', '助手'),
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, verbose_name='对话')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    content = models.TextField(verbose_name='内容')
    sources = models.JSONField(null=True, blank=True, verbose_name='引用来源')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['created_at']
