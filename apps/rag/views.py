from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Conversation, Message
from .services import get_rag_service


@login_required
def chat(request):
    """聊天界面"""
    conversations = Conversation.objects.filter(user=request.user)[:10]
    context = {
        'conversations': conversations,
    }
    return render(request, 'rag/chat.html', context)


@login_required
@require_POST
@csrf_exempt
def chat_api(request):
    """聊天 API"""
    try:
        data = json.loads(request.body)
        question = data.get('question', '')
        conversation_id = data.get('conversation_id')
        
        if not question:
            return JsonResponse({'error': '问题不能为空'}, status=400)
        
        # 获取或创建对话
        if conversation_id:
            conversation = Conversation.objects.get(
                id=conversation_id,
                user=request.user
            )
        else:
            conversation = Conversation.objects.create(
                user=request.user,
                title=question[:50]
            )
        
        # 保存用户消息
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=question
        )
        
        # RAG 查询
        rag_service = get_rag_service()
        result = rag_service.query(question)
        
        # 保存助手消息
        message = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=result['answer'],
            sources=result['sources']
        )
        
        return JsonResponse({
            'answer': result['answer'],
            'sources': result['sources'],
            'conversation_id': conversation.id,
            'message_id': message.id,
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def conversation_detail(request, pk):
    """对话详情"""
    conversation = Conversation.objects.get(pk=pk, user=request.user)
    messages = Message.objects.filter(conversation=conversation)
    
    context = {
        'conversation': conversation,
        'messages': messages,
    }
    return render(request, 'rag/conversation_detail.html', context)
