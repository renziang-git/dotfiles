#!/home/r.za/dotfiles/ai_env/bin/python
import os, sys, subprocess, tempfile, json, time, shutil
from datetime import datetime

# --- Config ---
# PROXY = "http://127.0.0.1:20171"
PIPER_MODEL = os.path.expanduser("~/piper-voices/en/en_US/lessac/low/en_US-lessac-low.onnx")
HISTORY_FILE = os.path.expanduser("~/.local/bin/tran/history.txt")
MPV_SOCKET = "/tmp/mpv-tts-socket"

# os.environ['http_proxy'] = PROXY
# os.environ['https_proxy'] = PROXY

# --- Core Functions ---

def speak(text, speed=1.5):
    subprocess.run(["pkill", "-f", "mpv"], stderr=subprocess.DEVNULL)
    if not text: return
    clean_text = str(text).strip().replace('"', '\\"').replace('$', '\\$')
    cmd = (f'echo "{clean_text}" | piper-tts --model {PIPER_MODEL} --length_scale {speed} --output_file - | '
           f'mpv - --no-video --input-ipc-server={MPV_SOCKET} --idle=no --msg-level=all=no')
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)

def clear_screen():
    print("\033[H\033[J", end="")

def smart_wrap(text, max_width=None):
    if max_width is None:
        max_width = shutil.get_terminal_size().columns - 4
    import re
    tokens = re.findall(r'[\u4e00-\u9fff]|[a-zA-Z0-9\-\']+|[^\u4e00-\u9fff\w]', str(text))
    lines, current_line, current_width = [], "", 0
    for token in tokens:
        token_width = sum(2 if ord(c) > 0x4e00 else 1 for c in token)
        if token_width > max_width:
            if current_line: lines.append(current_line)
            temp_token = token
            while temp_token:
                cut = max_width
                lines.append(temp_token[:cut])
                temp_token = temp_token[cut:]
            current_line, current_width = "", 0
            continue
        if current_width + token_width > max_width:
            lines.append(current_line.rstrip())
            current_line, current_width = token, token_width
        else:
            current_line += token
            current_width += token_width
    if current_line: lines.append(current_line.rstrip())
    return lines

def process_text(text, save=True):
    from pygtrans import Translate
    text = text.strip()
    if not text: return None
    try:
        # client = Translate(proxies={'http': PROXY, 'https': PROXY})
        client = Translate()
        res = client.translate(text, target='zh-CN', timeout=10)
        tran = str(res.translatedText).strip() if hasattr(res, 'translatedText') else str(res)
        if save: save_to_history(text, tran)
        speak(text)
        return (text, tran)
    except Exception as e:
        return (f"Error: {e}", "")

def save_to_history(original, translated):
    time_str = datetime.now().strftime("%m-%d %H:%M")
    line = f"[{time_str}] Or: {original} | Tr: {translated}\n"
    lines = [line]
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines += [l for l in f.readlines() if l.strip()]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines[:300])
        f.flush()
        os.fsync(f.fileno())

# --- Tools ---

def do_ocr(nest=False):
    from rapidocr_onnxruntime import RapidOCR
    print("📷 选择区域进行 OCR..."); 
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

def do_paste(nest=False, primary=False):
    cmd = ["wl-paste", "--primary"] if primary else ["wl-paste"]
    try:
        text = subprocess.check_output(cmd).decode().strip()
        data = process_text(text)
        if data:
            if nest: return data
            result_interface(data[0], data[1], "PRIMARY" if primary else "PASTE")
    except: return None

# --- Interfaces ---

def result_interface(orig, tran, mode_name):
    """TR"""
    while True:
        clear_screen()
        cols = shutil.get_terminal_size().columns
        print(f" {mode_name} ".center(cols, "-"))
        print(" [Or] ")
        for l in smart_wrap(orig): print(f" {l}")
        print("\n [Tr] ")
        for l in smart_wrap(tran): print(f" {l}")
        print("-" * cols)
        print(" 1.OCR  2.粘贴板  3.选中内容  4.停止音频  5.重新播放原文")
        print("ENTER")
        
        user_input = input("\n: ").strip()
        
        # 核心逻辑：如果输入为空（直接按了回车），跳出当前界面，回到主循环
        if not user_input:
            break
        
        if user_input == "1": 
            res = do_ocr(nest=True)
            if res: (orig, tran) = res
        elif user_input == "2": 
            res = do_paste(nest=True)
            if res: (orig, tran) = res
        elif user_input == "3": 
            res = do_paste(nest=True, primary=True)
            if res: (orig, tran) = res
        elif user_input == "4": 
            subprocess.run(["pkill", "-f", "mpv"])
        elif user_input == "5": 
            speak(orig) 
        else:
            # 输入了新文本，在此界面刷新翻译
            res = process_text(user_input)
            if res: orig, tran = res

def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("暂无历史记录"); time.sleep(1); return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    fzf_cmd = ["fzf", "--reverse", "--no-height", "--header=选择历史记录 (Esc 返回)", 
               "--preview=printf \"$(echo {} | sed -E 's/^.*Or: (.*) \\| Tr: (.*)$/\\1\\n\\2/')\"",
               "--preview-window=up:60%:wrap"]
    try:
        proc = subprocess.run(fzf_cmd, input="\n".join(lines).encode(), capture_output=True, check=True)
        selected = proc.stdout.decode().strip()
        if "Or: " in selected:
            orig = selected.split("Or: ")[1].split(" | Tr: ")[0]
            data = process_text(orig, save=False)
            if data: result_interface(data[0], data[1], "HISTORY")
    except: pass

def main():
    # 处理外部参数（快捷键触发）
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "respeak":
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    lines = [l for l in f.readlines() if l.strip()]
                    if lines:
                        first_line = lines[0]
                        if "Or: " in first_line:
                            orig = first_line.split("Or: ")[1].split(" | Tr: ")[0]
                            speak(orig)
            return

        if action == "stop":
            subprocess.run(["pkill", "-f", "mpv"])
            return

        # 快捷键 UI 模式：执行完后进入主循环，而不是退出
        initial_res = None
        if action == "ocr_ui": initial_res = do_ocr(nest=True)
        elif action == "paste_ui": initial_res = do_paste(nest=True)
        elif action == "primary_ui": initial_res = do_paste(nest=True, primary=True)
        
        if initial_res:
            result_interface(initial_res[0], initial_res[1], action.replace("_ui","").upper())
        
        # 如果是纯朗读模式（无 UI），执行完 return
        if action == "ocr":
            do_ocr(nest=True) # 内部会 speak
            return
        elif action in ["paste", "primary"]:
            do_paste(nest=True, primary=(action=="primary"))
            return

    # --- 主循环：永远不会主动退出 ---
    while True:
        clear_screen()
        cols = shutil.get_terminal_size().columns
        print("Translate".center(cols, "-"))
        print(" 1. OCR")
        print(" 2. Paste")
        print(" 3. Primary")
        print(" 4. Stop")
        print(" 5. History")
        print("-" * cols)
        
        val = input("Input:").strip().lower()
        
        # 即使输入为空或无效指令，也只是刷新主菜单
        if val == "1": do_ocr()
        elif val == "2": do_paste()
        elif val == "3": do_paste(primary=True)
        elif val == "4": subprocess.run(["pkill", "-f", "mpv"])
        elif val == "5": show_history()
        elif not val:
            continue
        else:
            data = process_text(val)
            if data: result_interface(data[0], data[1], "Translate")

if __name__ == "__main__":
    main()
