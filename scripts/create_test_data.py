#!/usr/bin/env python
"""
创建测试文档
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Document, Category, Tag

# 创建分类
pm_category = Category.objects.get_or_create(name='项目管理', defaults={'description': '项目管理相关知识'})[0]
agile_category = Category.objects.get_or_create(name='敏捷开发', defaults={'description': '敏捷方法论和实践'})[0]
risk_category = Category.objects.get_or_create(name='风险管理', defaults={'description': '项目风险识别和应对'})[0]

# 创建标签
tags = {}
for tag_name in ['PMP', 'Scrum', 'Agile', '风险', '规划', '团队']:
    tags[tag_name] = Tag.objects.get_or_create(name=tag_name)[0]

# 创建测试文档
documents = [
    {
        'title': '项目管理基础知识',
        'content': '''项目管理是指在项目活动中运用专门的知识、技能、工具和方法，使项目能够在有限资源限定条件下，实现或超过设定的需求和期望的过程。

项目管理的五大过程组：
1. 启动过程组 - 定义新项目或新阶段
2. 规划过程组 - 明确范围，优化目标
3. 执行过程组 - 完成工作，交付成果
4. 监控过程组 - 跟踪、审查和调整进展
5. 收尾过程组 - 正式完成项目

项目管理的十大知识领域：
- 范围管理
- 进度管理
- 成本管理
- 质量管理
- 资源管理
- 沟通管理
- 风险管理
- 采购管理
- 相关方管理
- 整合管理''',
        'summary': '介绍项目管理的基本概念、五大过程组和十大知识领域',
        'category': pm_category,
        'tags': [tags['PMP'], tags['规划']],
    },
    {
        'title': '敏捷开发方法论',
        'content': '''敏捷开发是一种以人为核心、迭代、循序渐进的开发方法。在敏捷开发中，软件项目的构建被切分成多个子项目，各个子项目的成果都经过测试，具备集成和可运行的特征。

敏捷宣言的四个核心价值观：
1. 个体和互动 > 流程和工具
2. 工作的软件 > 详尽的文档
3. 客户合作 > 合同谈判
4. 响应变化 > 遵循计划

Scrum 框架的三个角色：
- Product Owner (产品负责人)
- Scrum Master (敏捷教练)
- Development Team (开发团队)

Scrum 的四个仪式：
1. Sprint Planning (冲刺规划会)
2. Daily Standup (每日站会)
3. Sprint Review (冲刺评审会)
4. Sprint Retrospective (冲刺回顾会)''',
        'summary': '详解敏捷开发的核心价值观和 Scrum 框架',
        'category': agile_category,
        'tags': [tags['Scrum'], tags['Agile']],
    },
    {
        'title': '项目风险管理指南',
        'content': '''项目风险管理是项目管理中至关重要的环节，它包括风险识别、风险评估、风险应对和风险监控四个主要过程。

风险识别的方法：
1. 头脑风暴
2. 德尔菲技术
3. SWOT 分析
4. 核对单分析
5. 假设分析
6. 因果图分析

风险评估的维度：
- 发生概率（1-10 分）
- 影响程度（1-10 分）
- 风险分数 = 概率 × 影响

风险应对策略：
1. 规避 - 改变计划以消除风险
2. 转移 - 将风险转嫁给第三方
3. 减轻 - 降低概率或影响
4. 接受 - 承认风险并准备应急计划

风险监控要点：
- 定期审查已识别风险
- 识别新风险
- 评估风险应对措施的有效性
- 更新风险登记册''',
        'summary': '全面介绍项目风险管理的流程和方法',
        'category': risk_category,
        'tags': [tags['风险'], tags['PMP']],
    },
]

print("🍵 开始创建测试文档...")
for doc_data in documents:
    doc = Document.objects.create(
        title=doc_data['title'],
        content=doc_data['content'],
        summary=doc_data['summary'],
        category=doc_data['category'],
        is_public=True
    )
    for tag in doc_data['tags']:
        doc.tags.add(tag)
    print(f"✅ 创建文档：{doc.title}")

print(f"\n✅ 成功创建 {len(documents)} 篇测试文档！")
print("📚 现在可以访问 http://localhost:8000 查看基础知识库")
