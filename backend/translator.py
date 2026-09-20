import json
import os

from google import genai


client = genai.Client(api_key=os.environ["translate_API_KEY"])


def translate_to_english(texts: dict) -> dict:
    prompt = f"""
You are a professional academic translator.




Translate all values in the following JSON object from Traditional Chinese
into clear and natural academic English.

Requirements:
1. Preserve the original meaning exactly.
2. Do not summarize, explain, omit, or add information.
3. Preserve names, dates, URLs, technical terminology, and factual claims.
4. Preserve technical identifiers such as Rc, Rv, K_int, K_ext, pred_label, and reason.
5. Keep exactly the same JSON keys.
6. Return ONLY a valid JSON object.
7. Do not include Markdown code fences.

Input:
{json.dumps(texts, ensure_ascii=False)}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    translated = json.loads(text.strip())

    # 防止 Gemini 改掉或漏掉欄位
    if set(translated.keys()) != set(texts.keys()):
        raise ValueError(
            "Translation response keys do not match input keys."
        )

    return translated