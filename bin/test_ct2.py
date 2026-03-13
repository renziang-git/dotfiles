#!/usr/bin/env python3
import os
import ctranslate2
import sentencepiece as spm

# --- 模型路徑配置 ---
# 請確保此目錄下有 model.bin, source.spm, target.spm, config.json
MODEL_DIR = os.path.expanduser("~/models/opus-ct2")

def test_translation():
    print(f"🔄 正在載入模型：{MODEL_DIR} ...")
    
    try:
        # 1. 初始化翻譯器 (針對 X230 CPU 使用 int8 量化)
        #translator = ctranslate2.Translator(MODEL_DIR, device="cpu", compute_type="int8")
        translator = ctranslate2.Translator(MODEL_DIR,device="cpu",compute_type="int8"
)
        # 2. 載入 SentencePiece 編碼器
        sp_source = spm.SentencePieceProcessor(os.path.join(MODEL_DIR, "source.spm"))
        sp_target = spm.SentencePieceProcessor(os.path.join(MODEL_DIR, "target.spm"))
        
        print("✅ 模型載入成功！")

        # 3. 測試文本
        test_sentences = [
            ".To install the package, you need to run the command with sudo privileges and ensure that all dependencies are met.",
            "Although the initial setup of Arch Linux can be challenging for beginners, the level of control and customization it offers makes it one of the most rewarding distributions for advanced users.",
            "The kernel is the core of the operating system, managing the communication between hardware and software components."

        ]

        print("\n🚀 開始翻譯測試：")
        for text in test_sentences:
            # A. 編碼 (將文字轉為 Token)
            source_tokens = sp_source.encode(text, out_type=str)
            
            # B. 翻譯 (CT2 引擎運算)
            results = translator.translate_batch([source_tokens])
            
            # C. 解碼 (將 Token 轉回文字)
            translated_text = sp_target.decode(results[0].hypotheses[0])
            
            print(f"\n[原文]: {text}")
            print(f"[譯文]: {translated_text}")

    except Exception as e:
        print(f"\n❌ 測試失敗：{e}")
        print("\n💡 請檢查 ~/models/opus-ct2/ 目錄下是否包含所需的 4 個檔案。")

if __name__ == "__main__":
    test_translation()
