"""
RAG 服务 - 基于 LangChain + Chroma + 智谱嵌入模型
"""
import os
import chromadb
from chromadb.config import Settings
from openai import OpenAI
from django.conf import settings
from typing import List, Dict, Any


class RAGService:
    """RAG 服务类"""
    
    def __init__(self):
        # 初始化智谱 LLM 和嵌入模型（使用同一个 API）
        self.llm_client = OpenAI(
            api_key=settings.ZHIPU_API_KEY,
            base_url=settings.ZHIPU_API_BASE
        )
        self.llm_model = settings.ZHIPU_LLM_MODEL
        
        # 智谱嵌入模型
        self.embedding_model_name = "embedding-2"
        
        # 初始化 Chroma 向量数据库
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="pm_knowledge",
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_embedding(self, text: str) -> List[float]:
        """获取文本的向量嵌入（使用智谱 API）"""
        response = self.llm_client.embeddings.create(
            model=self.embedding_model_name,
            input=text
        )
        return response.data[0].embedding
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """添加文档到向量数据库"""
        ids = []
        embeddings = []
        metadatas = []
        contents = []
        
        for i, doc in enumerate(documents):
            doc_id = f"doc_{doc.get('id', i)}"
            ids.append(doc_id)
            embeddings.append(self.get_embedding(doc['content']))
            metadatas.append({
                'title': doc.get('title', ''),
                'source': doc.get('source', ''),
            })
            contents.append(doc['content'])
        
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=contents
        )
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        query_embedding = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # 格式化结果
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                search_results.append({
                    'content': doc,
                    'title': results['metadatas'][0][i].get('title', ''),
                    'source': results['metadatas'][0][i].get('source', ''),
                    'score': 1 - results['distances'][0][i],  # 转换为相似度分数
                })
        
        return search_results
    
    def generate_answer(self, query: str, context: str) -> str:
        """使用 LLM 生成答案"""
        prompt = f"""你是一个专业的项目管理助手。请根据以下参考资料回答问题。

参考资料：
{context}

问题：{query}

请用中文专业、简洁地回答。如果资料中没有相关信息，请说明。"""

        response = self.llm_client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "你是一个专业的项目管理助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """完整的 RAG 查询流程"""
        # 1. 搜索相关文档
        search_results = self.search(question, top_k)
        
        # 2. 构建上下文
        context = "\n\n".join([
            f"【{r['title']}】\n{r['content']}"
            for r in search_results
        ])
        
        # 3. 生成答案
        answer = self.generate_answer(question, context)
        
        return {
            'answer': answer,
            'sources': search_results,
        }


# 单例模式
rag_service = None

def get_rag_service() -> RAGService:
    """获取 RAG 服务单例"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service
