from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from model.models import db


async def process_user_question(content: str):
    # 更新后的知识点查询
    knowledge_points_collection = db["knowledge_points"]
    knowledge_points = await knowledge_points_collection.find().to_list(length=None)

    matched_knowledge = []
    for point in knowledge_points:
        # 根据用户问题匹配知识点的名称
        if any(keyword in content for keyword in point.get('name', [])):
            matched_knowledge.append(point)

    # 如果未匹配到知识点，返回默认信息
    if not matched_knowledge:
        return [{
            "content": "未找到相关知识点。",
            "attachments": [],
            "iframe": None,
            "bilibili_iframe": None
        }]

    # 调用星火大模型获取回答
    chat = ChatSparkLLM(
        spark_app_id="4bd69419",
        spark_api_key="f0a405aace81ed2ec920f20dc2299648",
        spark_api_secret="NDZiNTk5ZDg5OTNlMDk3M2IzZTEwMzMy",
        spark_api_url="wss://spark-api.xf-yun.com/v3.5/chat",
        spark_llm_domain="generalv3.5"
    )

    messages = [ChatMessage(role="user", content=content)]
    handler = ChunkPrintHandler()
    response = await chat.generate([messages], callbacks=[handler])
    content_response = response  # 提取模型的回答内容

    # 组装返回数据
    message_data = []
    for knowledge in matched_knowledge:
        attachments = []

        # 如果资源的结构变化，这里需要根据新的结构进行更新
        for resource in knowledge.get('resource', []):
            if resource.get('type') in ['pdf', 'word']:
                attachments.append({
                    "id": resource.get('value'),  # 使用 UUID 作为资源唯一标识
                    "type": resource.get('type')
                })

        # 处理 iframe 和 bilibili 资源类型
        iframe = next(
            (res['value'] for res in knowledge.get('resource', []) if res.get('type') == 'animation_iframe'),
            None
        )
        bilibili_iframe = next(
            (res['value'] for child in knowledge.get('children', [])
             for res in child.get('resource', []) if res.get('type') == 'bilibili'),
            None
        )

        message_data.append({
            "content": content_response,  # 模型返回的内容
            "attachments": attachments,
            "iframe": iframe,
            "bilibili_iframe": bilibili_iframe
        })

    return message_data
