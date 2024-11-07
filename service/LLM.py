from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from model.models import knowledge_points_collection


async def process_user_question(content: str):
    # 查询知识点匹配用户问题
    knowledge_points = knowledge_points_collection.find()

    matched_knowledge = []
    for point in knowledge_points:
        if any(keyword in content for keyword in point['name']):
            matched_knowledge.append(point)

    if not matched_knowledge:
        return [{"content": "未找到相关知识点。", "attachments": [], "iframe": None, "bilibili_iframe": None}]

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
    content_response = response  # 根据模型返回的结果提取内容

    # 组装返回数据
    message_data = []
    for knowledge in matched_knowledge:
        attachments = []
        for resource in knowledge['resource']:
            if resource['type'] in ['pdf', 'word']:
                attachments.append({
                    "id": resource['value'],  # 这里是 UUID
                    "type": resource['type']
                })

        message_data.append({
            "content": content_response,  # 模型返回的内容
            "attachments": attachments,
            "iframe": next((res['value'] for res in knowledge['resource'] if res['type'] == 'animation_iframe'), None),
            "bilibili_iframe": next(
                (res['value'] for res in knowledge['children'] for res in res['resource'] if res['type'] == 'bilibili'),
                None)
        })

    return message_data