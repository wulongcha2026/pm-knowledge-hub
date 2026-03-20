from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import RiskAssessment, RiskItem
from .services import get_risk_agent


@login_required
def index(request):
    """风险评估列表"""
    assessments = RiskAssessment.objects.filter(user=request.user)
    context = {
        'assessments': assessments,
    }
    return render(request, 'risk_agent/index.html', context)


@login_required
def create(request):
    """创建风险评估"""
    return render(request, 'risk_agent/create.html')


@login_required
@require_POST
@csrf_exempt
def analyze_api(request):
    """风险分析 API"""
    try:
        data = json.loads(request.body)
        title = data.get('title', '风险评估')
        project_description = data.get('project_description', '')
        meeting_notes = data.get('meeting_notes', '')
        
        if not project_description:
            return JsonResponse({'error': '项目描述不能为空'}, status=400)
        
        # 创建评估记录
        assessment = RiskAssessment.objects.create(
            user=request.user,
            title=title,
            project_description=project_description,
            meeting_notes=meeting_notes,
            status='analyzing'
        )
        
        # 执行风险分析
        risk_agent = get_risk_agent()
        result = risk_agent.analyze(project_description, meeting_notes)
        
        # 保存风险项
        for risk_data in result['risk_items']:
            RiskItem.objects.create(
                assessment=assessment,
                category=risk_data.get('category', 'technical'),
                title=risk_data.get('title', ''),
                description=risk_data.get('description', ''),
                risk_level=risk_data.get('risk_level', 'medium'),
                probability=risk_data.get('probability', 5),
                impact=risk_data.get('impact', 5),
                mitigation_suggestions=risk_data.get('mitigation_suggestions', '')
            )
        
        # 更新评估状态
        assessment.overall_risk_level = result['overall_risk_level']
        assessment.status = 'completed'
        assessment.save()
        
        return JsonResponse({
            'assessment_id': assessment.id,
            'overall_risk_level': result['overall_risk_level'],
            'risk_count': len(result['risk_items']),
            'analysis_steps': result['analysis_steps'],
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def detail(request, pk):
    """风险评估详情"""
    assessment = get_object_or_404(RiskAssessment, pk=pk, user=request.user)
    risk_items = RiskItem.objects.filter(assessment=assessment)
    
    context = {
        'assessment': assessment,
        'risk_items': risk_items,
    }
    return render(request, 'risk_agent/detail.html', context)
