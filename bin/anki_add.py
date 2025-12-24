#!/usr/bin/env python3
import requests
import subprocess
import re

ANKI_URL = "http://localhost:8765"

# -------------------------------------------------------
# 1. 稳定的剪贴板读取：clipboard → primary → copyq
# -------------------------------------------------------
def get_clipboard():
    # Try clipboard (Ctrl+C)
    try:
        p = subprocess.run(
            ["xclip", "-o", "-selection", "clipboard"],
            capture_output=True, text=True
        )
        if p.stdout.strip():
            return p.stdout.strip()
    except:
        pass

    # Try primary (mouse selection)
    try:
        p = subprocess.run(
            ["xclip", "-o", "-selection", "primary"],
            capture_output=True, text=True
        )
        if p.stdout.strip():
            return p.stdout.strip()
    except:
        pass

    # Try CopyQ
    try:
        p = subprocess.run(
            ["copyq", "clipboard"],
            capture_output=True, text=True
        )
        if p.stdout.strip():
            return p.stdout.strip()
    except:
        pass

    return ""


# -------------------------------------------------------
# 2. 中文释义 - Youdao
# -------------------------------------------------------
def zh_def(word):
    url = f"https://dict.youdao.com/result?word={word}&lang=en"
    try:
        html = requests.get(url, timeout=3).text
        m = re.findall(r'<span class="trans">(.*?)</span>', html)
        return "; ".join(m[:3]) if m else ""
    except Exception as e:
        print("Youdao error:", e)
        return ""


# -------------------------------------------------------
# 3. 英英释义 - Cambridge
# -------------------------------------------------------
def en_def(word):
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=4).text
        defs = re.findall(r'definition">([^<]+)<', html)
        return defs[0] if defs else ""
    except Exception as e:
        print("Cambridge EN error:", e)
        return ""


# -------------------------------------------------------
# 4. 音标 - Cambridge
# -------------------------------------------------------
def ipa(word):
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=4).text
        m = re.findall(r'ipa">(.*?)<', html)
        return m[0] if m else ""
    except Exception as e:
        print("Cambridge IPA error:", e)
        return ""


# -------------------------------------------------------
# 5. 添加到 Anki
# -------------------------------------------------------
def push_anki(front, back, ipa_code, sentence, source):
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "English",
                "modelName": "English-Advanced",
                "fields": {
                    "Front": front,
                    "Back": back,
                    "IPA": ipa_code,
                    "Sentence": sentence,
                    "Source": source
                },
                "audio": []  # 使用 HyperTTS 自动生成
            }
        }
    }

    r = requests.post(ANKI_URL, json=payload)
    print("Status:", r.status_code)
    print("Response:", r.text)


# -------------------------------------------------------
# 6. 主流程
# -------------------------------------------------------
def main():
    text = get_clipboard()
    print("Clipboard:", text)

    if not text.strip():
        print("Error: Clipboard is empty.")
        return

    # 提取英文单词（如果是句子，取第一个英文单词）
    words = re.findall(r"[A-Za-z\-']+", text)
    word = words[0].lower() if words else text.strip()
    print("Word:", word)

    zh = zh_def(word)
    print("ZH:", zh)

    en = en_def(word)
    print("EN:", en)

    ipa_code = ipa(word)
    print("IPA:", ipa_code)

    # 生成 Back 字段
    back = ""
    if zh:
        back += f"<b>中文释义：</b> {zh}<br>"
    if en:
        back += f"<b>英英释义：</b> {en}<br>"

    push_anki(
        front=word,
        back=back,
        ipa_code=ipa_code,
        sentence=text,
        source="Clipboard"
    )


if __name__ == "__main__":
    main()

