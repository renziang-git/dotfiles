#!/home/r.za/dotfiles/ai_env/bin/python
"""
tran-client.py - 翻译客户端
快捷键调用，发送请求给守护进程（不加载模型，响应极快）
"""

import os
import sys
import socket
import subprocess
import tempfile
import json
from datetime import datetime

# ============================================================
# 配置
# ============================================================
SOCKET_PATH = "/tmp/tran-daemon.sock"
HISTORY_FILE = os.path.expanduser("~/dotfiles/bin/tran/history.txt")


def send_to_daemon(action, text="", speed=1.5):
    """发送请求给守护进程"""
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5秒超时
        sock.connect(SOCKET_PATH)

        request = json.dumps({
            'action': action,
            'text': text,
            'speed': speed
        })
        sock.send(request.encode())
        result = sock.recv(1024)
        sock.close()
        return result == b'OK'
    except FileNotFoundError:
        print("❌ 守护进程未运行！请先启动: python3 tran-daemon.py &", file=sys.stderr)
        return False
    except socket.timeout:
        print("❌ 守护进程响应超时", file=sys.stderr)
        return False
    except Exception as e:
        print(f"❌ 连接守护进程失败: {e}", file=sys.stderr)
        return False


def speak(text):
    """朗读文本（通过守护进程）"""
    if not text:
        return False
    return send_to_daemon('speak', text)


def stop_audio():
    """停止音频"""
    return send_to_daemon('stop')


def translate_and_speak(text, save=True):
    """翻译文本并朗读"""
    from pygtrans import Translate

    text = str(text).strip()
    if not text:
        return None

    try:
        client = Translate()
        res = client.translate(text, target='zh-CN', timeout=10)
        tran = str(res.translatedText).strip() if hasattr(res, 'translatedText') else str(res)

        if save:
            save_to_history(text, tran)

        # 通过守护进程朗读原文
        speak(text)

        return (text, tran)
    except Exception as e:
        print(f"❌ 翻译错误: {e}", file=sys.stderr)
        return None


def save_to_history(original, translated):
    """保存翻译历史"""
    time_str = datetime.now().strftime("%m-%d %H:%M")
    line = f"[{time_str}] Or: {original} | Tr: {translated}\n"

    lines = [line]
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines += [l for l in f.readlines() if l.strip()]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines[:300])


def do_ocr():
    """OCR 识别并翻译"""
    from rapidocr_onnxruntime import RapidOCR

    print("📷 选择区域进行 OCR...", file=sys.stderr)
    try:
        region = subprocess.check_output(["slurp"]).decode().strip()
        tmp = os.path.join(tempfile.gettempdir(), "ocr.png")
        subprocess.run(["grim", "-g", region, tmp], check=True)

        res, _ = RapidOCR()(tmp)
        if res:
            text = " ".join([str(item[1]) for item in res])
            if text.strip():
                return translate_and_speak(text)
        print("⚠️ OCR 未识别到文字", file=sys.stderr)
    except subprocess.CalledProcessError:
        print("❌ OCR 区域选择失败", file=sys.stderr)
    except Exception as e:
        print(f"❌ OCR 错误: {e}", file=sys.stderr)
    return None


def do_paste(primary=False):
    """获取剪贴板内容并翻译"""
    cmd = ["wl-paste", "--primary"] if primary else ["wl-paste"]
    try:
        text = subprocess.check_output(cmd).decode().strip()
        if text:
            return translate_and_speak(text)
        print("⚠️ 剪贴板为空", file=sys.stderr)
    except subprocess.CalledProcessError:
        print("❌ 获取剪贴板失败", file=sys.stderr)
    except Exception as e:
        print(f"❌ 粘贴板错误: {e}", file=sys.stderr)
    return None


def respeak_last():
    """重读最后一条历史"""
    if not os.path.exists(HISTORY_FILE):
        print("⚠️ 暂无历史记录", file=sys.stderr)
        return

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if "Or: " in line:
                orig = line.split("Or: ")[1].split(" | Tr: ")[0]
                speak(orig)
                print(f"🔊 重读: {orig[:50]}...", file=sys.stderr)
                return
    print("⚠️ 未找到历史记录", file=sys.stderr)


def show_notification(title, message):
    """发送桌面通知"""
    try:
        subprocess.run(
            ['notify-send', title, message, '-t', '2000'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    except:
        pass


def main():
    if len(sys.argv) < 2:
        print("用法: tran-client.py [ocr|paste|primary|stop|respeak]", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1]

    if action == "stop":
        stop_audio()
        return

    if action == "respeak":
        respeak_last()
        return

    # 执行翻译操作
    result = None
    if action == "ocr":
        result = do_ocr()
    elif action == "paste":
        result = do_paste()
    elif action == "primary":
        result = do_paste(primary=True)
    else:
        print(f"❌ 未知操作: {action}", file=sys.stderr)
        sys.exit(1)

    # 输出译文到 stdout（供 fzf/rofi 等捕获）
    if result:
        print(result[1])  # 只输出译文
        show_notification("翻译", result[1][:100])
    else:
        print("❌ 翻译失败", file=sys.stderr)
        show_notification("翻译失败", "请检查网络或重试")


if __name__ == "__main__":
    main()
