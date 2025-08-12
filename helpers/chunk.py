def split_transcript(text, chunk_size=700):
    """
    將長字串等分切片，每段不超過 chunk_size
    """
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def extract_keywords_from_chunk(chunk, llm_api_call):
    """
    chunk: 字串片段
    llm_api_call: 你包裝的 LLM API 函式，必須回傳 [{'keyword': ..., 'explanation': ...}, ...]
    """
    prompt = (
        "請閱讀以下內容，萃取所有重要專有名詞與知識點（以列表表示，每項標註關鍵詞與解釋）：\n"
        f"{chunk}\n"
        "請回傳格式：[{'keyword':..., 'explanation':...}, ...]"
    )
    result = llm_api_call(prompt)
    return result  # [{"keyword": "Zeroshot Prompt", "explanation": "..."}, ...]

def batch_extract_keywords(transcript, llm_api_call, chunk_size=700):
    chunks = split_transcript(transcript, chunk_size)
    all_keywords = []
    for chunk in chunks:
        keywords = extract_keywords_from_chunk(chunk, llm_api_call)
        all_keywords.extend(keywords)
    return all_keywords

def deduplicate_keywords(keywords_list):
    """
    針對所有關鍵詞去重，簡單實作：同名（小寫比對）視為同一詞，解釋取最長或最完整
    """
    keyword_map = {}
    for kw in keywords_list:
        key = kw["keyword"].strip().lower()
        if key not in keyword_map:
            keyword_map[key] = kw
        else:
            # 如有不同解釋，以最長的為主
            if len(kw["explanation"]) > len(keyword_map[key]["explanation"]):
                keyword_map[key] = kw
    return list(keyword_map.values())

def full_transcript_keyword_pipeline(transcript, llm_api_call):
    # 1. 分段，2. 關鍵詞抽取，3. 合併去重
    all_keywords = batch_extract_keywords(transcript, llm_api_call)
    unique_keywords = deduplicate_keywords(all_keywords)
    return unique_keywords