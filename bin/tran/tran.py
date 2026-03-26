#!/home/r.za/dotfiles/ai_env/bin/python
import os, sys, subprocess, tempfile, json, time, shutil
from datetime import datetime

# --- Config ---
PROXY = "http://127.0.0.1:20171"
PIPER_MODEL = os.path.expanduser("~/models/tts/en_US-lessac-low.onnx")
HISTORY_FILE = os.path.expanduser("~/dotfiles/bin/tran/history.txt")
MPV_SOCKET = "/tmp/mpv-tts-socket"

os.environ['http_proxy'] = PROXY
os.environ['https_proxy'] = PROXY

# --- Core Functions ---

def speak(text, speed=1.2):
    subprocess.run(["pkill", "-f", "mpv"], stderr=subprocess.DEVNULL)
    if not text: return
    clean_text = str(text).strip().replace('"', '\\"')
    cmd = (f'echo "{clean_text}" | piper-tts --model {PIPER_MODEL} --length_scale {speed} --output_file - | '
           f'mpv - --no-video --input-ipc-server={MPV_SOCKET} --idle=no --msg-level=all=no')
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)

def send_mpv_command(command):
    if not os.path.exists(MPV_SOCKET): return
    msg = json.dumps({"command": command}).encode() + b"\n"
    try:
        subprocess.run(["socat", "-", f"UNIX-CONNECT:{MPV_SOCKET}"], input=msg, capture_output=True, timeout=0.5)
    except: pass

def save_to_history(original, translated):
    time_str = datetime.now().strftime("%m-%d %H:%M")
    line = f"[{time_str}] Or: {original} | Tr: {translated}\n"
    lines = [line]
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines += [l for l in f.readlines() if l.strip()]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines[:300])

def smart_wrap(text, max_width=None):
    """
    智能折行：英文按单词断行，中文按字符断行
    """
    if max_width is None:
        # 预留 4 个字符宽度作为左右边距
        max_width = shutil.get_terminal_size().columns - 4
    
    import re
    # 将文本切分为：中文序列、英文单词、空格、符号
    # \u4e00-\u9fff 是中文区间
    tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9\-\']+|[^\u4e00-\u9fff\w]', str(text))
    
    lines = []
    current_line = ""
    current_width = 0
    
    for token in tokens:
        # 计算当前 token 的显示宽度
        # 中文占 2 宽，其他（英文/符号）通常占 1 宽
        token_width = sum(2 if ord(c) > 0x4e00 else 1 for c in token)
        
        # 如果单个 token 超过最大宽度（极长单词），强制截断
        if token_width > max_width:
            if current_line: lines.append(current_line)
            # 对超长 token 强制按宽度切割
            temp_token = token
            while temp_token:
                cut = max_width
                lines.append(temp_token[:cut])
                temp_token = temp_token[cut:]
            current_line, current_width = "", 0
            continue

        # 如果当前行加上这个 token 超过了最大宽度
        if current_width + token_width > max_width:
            lines.append(current_line.rstrip()) # 去掉行末空格
            current_line = token
            current_width = token_width
        else:
            current_line += token
            current_width += token_width
            
    if current_line:
        lines.append(current_line.rstrip())
        
    return lines

def process_text(text, save=True):
    from pygtrans import Translate
    text = text.strip()
    if not text: return None
    try:
        client = Translate(proxies={'http': PROXY, 'https': PROXY})
        res = client.translate(text, target='zh-CN', timeout=10)
        tran = str(res.translatedText).strip() if hasattr(res, 'translatedText') else str(res)
        if save: save_to_history(text, tran)
        speak(text)
        return (text, tran)
    except Exception as e:
        return (f"Error: {e}", "")

def clear_screen():
    print("\033[H\033[J", end="")

# --- Interfaces ---

def result_interface(orig, tran, mode_name):
    """标准的控制台交互界面"""
    while True:
        clear_screen()
        cols = shutil.get_terminal_size().columns
        print(f" {mode_name} ".center(cols, "-"))
        print(" [Original] ")
        for l in smart_wrap(orig): print(f" {l}")
        print("\n [Translation] ")
        for l in smart_wrap(tran): print(f" {l}")
        print("-" * cols)
        print(" 1.Speak  2.Pause/Res  3.Copy  4.OCR  5.Paste  6.Back")
        
        user_input = input("\n[Input Text or Select #]: ").strip()
        if not user_input: continue
        
        if user_input == "1": speak(orig)
        elif user_input == "2": send_mpv_command(["cycle", "pause"])
        elif user_input == "3":
            subprocess.run(["wl-copy"], input=f"{orig}\n{tran}".encode())
        elif user_input == "4":
            res = do_ocr(nest=True)
            if res: orig, tran = res
        elif user_input == "5":
            res = do_paste(nest=True)
            if res: orig, tran = res
        elif user_input == "6": break
        else:
            res = process_text(user_input)
            if res: orig, tran = res

def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("No history found."); time.sleep(1); return

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    fzf_cmd = [
        "fzf",
        "--reverse",
        "--no-height",
        "--header=Select History (ENTER: View | ESC: Back)",
        # 修正对齐问题的预览命令
        "--preview=printf \"$(echo {} | sed -E 's/^.*Or: (.*) \| Tr: (.*)$/\\1\\n\\2/')\"",
        "--preview-window=up:60%:wrap",
        "--ellipsis=",
        "--no-unicode"
    ]

    try:
        proc = subprocess.run(fzf_cmd, input="\n".join(lines).encode(), capture_output=True, check=True)
        selected = proc.stdout.decode().strip()
        if "Or: " in selected:
            orig = selected.split("Or: ")[1].split(" | Tr: ")[0]
            data = process_text(orig, save=False)
            if data:
                result_interface(data[0], data[1], "History")
    except subprocess.CalledProcessError:
        pass

# --- Tools ---

def speak_paste():
    """纯朗读剪贴板内容，不翻译"""
    try:
        text = subprocess.check_output(["wl-paste"]).decode("utf-8").strip()
        if text:
            print(f"[Speaking Clipboard]: {text[:50]}...")
            speak(text)
    except Exception as e:
        print(f"Error: {e}")

def speak_ocr():
    """OCR 识别后纯朗读，不翻译"""
    from rapidocr_onnxruntime import RapidOCR
    print("📷 Select region for TTS...") 
    try:
        region = subprocess.check_output(["slurp"]).decode().strip()
        tmp = os.path.join(tempfile.gettempdir(), "ocr_tts.png")
        subprocess.run(["grim", "-g", region, tmp], check=True)
        res, _ = RapidOCR()(tmp)
        if res:
            text = " ".join([str(item[1]) for item in res])
            print(f"[Speaking OCR]: {text[:50]}...")
            speak(text)
    except Exception as e:
        print(f"Error: {e}")

def do_ocr(nest=False):
    from rapidocr_onnxruntime import RapidOCR
    print("📷 Select region..."); 
    try:
        region = subprocess.check_output(["slurp"]).decode().strip()
        tmp = os.path.join(tempfile.gettempdir(), "ocr.png")
        subprocess.run(["grim", "-g", region, tmp], check=True)
        res, _ = RapidOCR()(tmp)
        if res:
            text = " ".join([str(item[1]) for item in res])
            data = process_text(text)
            if data:
                if nest: return data
                result_interface(data[0], data[1], "OCR")
    except: return None

def do_paste(nest=False):
    try:
        text = subprocess.check_output(["wl-paste"]).decode().strip()
        data = process_text(text)
        if data:
            if nest: return data
            result_interface(data[0], data[1], "Paste")
    except: return None

def main():
    # --- 1. 处理 Niri 快捷键传来的参数 (后台静默运行) ---
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        # --- 划词朗读 (Primary Selection) ---
        if action == "primary":
            try:
                # 获取鼠标抹黑的内容
                text = subprocess.check_output(["wl-paste", "--primary"]).decode("utf-8").strip()
                if text:
                    speak(text)
            except:
                pass
            return # 执行完直接退出
        elif action == "ocr":
            from rapidocr_onnxruntime import RapidOCR
            try:
                # 选区并截图
                region = subprocess.check_output(["slurp"]).decode().strip()
                tmp = os.path.join(tempfile.gettempdir(), "ocr_tts.png")
                subprocess.run(["grim", "-g", region, tmp], check=True)
                # 识别文字
                res, _ = RapidOCR()(tmp)
                if res:
                    text = " ".join([str(item[1]) for item in res])
                    speak(text)  # 直接朗读，不翻译
            except: pass
            return # 执行完直接退出，不弹窗口

        elif action == "paste":
            try:
                text = subprocess.check_output(["wl-paste"]).decode("utf-8").strip()
                if text: speak(text) # 直接朗读剪贴板
            except: pass
            return

        elif action == "stop":
            subprocess.run(["pkill", "-f", "mpv"])
            return

        elif action == "pause":
            send_mpv_command(["cycle", "pause"])
            return

    # --- 2. 如果没有参数，进入原本的交互式菜单 (手动操作模式) ---
    while True:
        clear_screen()
        cols = shutil.get_terminal_size().columns
        print(" Translation Helper ".center(cols, "-"))
        print(" 1. OCR (Screen)")
        print(" 2. Paste (Clipboard)")
        print(" 3. Stop Audio")
        print(" 4. History (FZF)")
        print(" 5. Exit")
        print("-" * cols)
        
        val = input("[Input Text or Select #]: ").strip()
        if not val: continue
        
        if val == "1": do_ocr()
        elif val == "2": do_paste()
        elif val == "3": subprocess.run(["pkill", "-f", "mpv"])
        elif val == "4": show_history()
        elif val == "5": break
        else:
            data = process_text(val)
            if data: result_interface(data[0], data[1], "Quick Translate")

if __name__ == "__main__":
    main()
