from django.db import models
from django.contrib.auth.models import User


class RiskAssessment(models.Model):
    """风险评估"""
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('analyzing', '分析中'),
        ('completed', '已完成'),
    ]
    
    RISK_LEVELS = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('critical', '严重'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=200, verbose_name='评估标题')
    project_description = models.TextField(verbose_name='项目描述')
    meeting_notes = models.TextField(blank=True, verbose_name='会议纪要')
    overall_risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        null=True,
        blank=True,
        verbose_name='整体风险等级'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '风险评估'
        verbose_name_plural = '风险评估'
        ordering = ['-created_at']


class RiskItem(models.Model):
    """风险项"""
    CATEGORY_CHOICES = [
        ('technical', '技术风险'),
        ('schedule', '进度风险'),
        ('resource', '资源风险'),
        ('requirement', '需求风险'),
        ('communication', '沟通风险'),
        ('external', '外部风险'),
    ]
    
    assessment = models.ForeignKey(
        RiskAssessment,
        on_delete=models.CASCADE,
        related_name='risk_items',
        verbose_name='风险评估'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='风险类别'
    )
    title = models.CharField(max_length=200, verbose_name='风险标题')
    description = models.TextField(verbose_name='风险描述')
    risk_level = models.CharField(
        max_length=20,
        choices=RiskAssessment.RISK_LEVELS,
        verbose_name='风险等级'
    )
    probability = models.IntegerField(
        default=5,
        help_text='1-10，发生概率',
        verbose_name='发生概率'
    )
    impact = models.IntegerField(
        default=5,
        help_text='1-10，影响程度',
        verbose_name='影响程度'
    )
    mitigation_suggestions = models.TextField(verbose_name='应对建议')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '风险项'
        verbose_name_plural = '风险项'
        ordering = ['risk_level']
