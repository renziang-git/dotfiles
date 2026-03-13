import os
import subprocess
from rapidocr_onnxruntime import RapidOCR

# 1. 設置臨時圖片路徑
temp_img = "/home/r.za/models/ocr/ocr_test.png"

def run_test():
    # 2. 呼叫 Wayland 截圖工具 (grim + slurp)
    # 執行後，你的滑鼠會變成十字準星，請拉出一個包含文字的範圍
    print("🎯 請用滑鼠拖曳選取一段文字區域...")
    try:
        subprocess.run(f'grim -g "$(slurp)" {temp_img}', shell=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ 截圖被取消或發生錯誤")
        return

    # 3. 初始化 RapidOCR 引擎 (在 X230 上這步非常快)
    # 第一次執行會下載模型，請保持網路連線
    engine = RapidOCR()

    # 4. 進行識別
    print("🌀 正在識別文字...")
    results, _ = engine(temp_img)

    # 5. 輸出結果
    if results:
        print("\n✅ --- 識別成功 ---")
        for line in results:
            # 確保取得的是文字與信心度
            # RapidOCR 每一行格式：[ [坐標], "文字", 信心度 ]
            text = line[1]
            try:
                conf = float(line[2]) # 強制轉為浮點數
                print(f"內容: {text} (信心度: {conf:.2f})")
            except (ValueError, IndexError):
                print(f"內容: {text}")
        print("-------------------\n")
        
    # 6. 清理
    if os.path.exists(temp_img):
        os.remove(temp_img)

if __name__ == "__main__":
    run_test()
