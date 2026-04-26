#!/home/r.za/dotfiles/ai_env/bin/python
"""
tran-daemon.py - Piper TTS 守护进程
常驻内存，响应客户端请求
启动方式：python3 tran-daemon.py &
"""

import os
import sys
import socket
import tempfile
import threading
import subprocess
import wave
import json
import signal
import atexit

# Piper TTS
from piper import PiperVoice

# ============================================================
# 配置（与你的原脚本保持一致）
# ============================================================
PIPER_MODEL = os.path.expanduser("~/models/tts/en_US-lessac-low.onnx")
SOCKET_PATH = "/tmp/tran-daemon.sock"
MPV_SOCKET = "/tmp/mpv-tts-socket"

# 全局变量
_piper_voice = None
_piper_sample_rate = 22050
_server_socket = None


def get_piper_voice():
    """加载 Piper 模型（只一次）"""
    global _piper_voice, _piper_sample_rate
    if _piper_voice is None:
        print("[Daemon] 正在加载 Piper 模型...", flush=True)
        print(f"[Daemon] 模型路径: {PIPER_MODEL}", flush=True)
        _piper_voice = PiperVoice.load(PIPER_MODEL)
        _piper_sample_rate = _piper_voice.config.sample_rate
        print("[Daemon] ✅ Piper 模型加载完成", flush=True)
    return _piper_voice


def speak(text, speed=1.5):
    """合成并播放音频"""
    if not text or not str(text).strip():
        return False

    clean_text = str(text).strip()

    # 停止当前播放的 mpv
    subprocess.run(["pkill", "-f", "mpv"], stderr=subprocess.DEVNULL)

    voice = get_piper_voice()

    # 合成到临时 WAV 文件
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        with wave.open(tmp_path, 'wb') as wav_file:
            voice.synthesize_wav(clean_text, wav_file, length_scale=speed)

        # 播放
        subprocess.Popen(
            ['mpv', tmp_path, '--no-video', '--input-ipc-server=' + MPV_SOCKET,
             '--really-quiet'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid if hasattr(os, 'setsid') else None
        )
        # 延迟删除临时文件
        threading.Timer(5.0, lambda: os.unlink(tmp_path) if os.path.exists(tmp_path) else None).start()
        return True
    except Exception as e:
        print(f"[Daemon] TTS 错误: {e}", flush=True)
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        return False


def stop_audio():
    """停止播放"""
    subprocess.run(["pkill", "-f", "mpv"], stderr=subprocess.DEVNULL)
    return True


def handle_client(conn):
    """处理客户端请求"""
    try:
        data = conn.recv(4096).decode('utf-8')
        if not data:
            return

        request = json.loads(data)
        action = request.get('action')
        text = request.get('text', '')
        speed = request.get('speed', 1.5)

        print(f"[Daemon] 收到请求: {action}, text={text[:50]}...", flush=True)

        if action == 'speak':
            success = speak(text, speed)
            conn.send(b'OK' if success else b'ERROR')
        elif action == 'stop':
            stop_audio()
            conn.send(b'OK')
        else:
            conn.send(f'ERROR: unknown action {action}'.encode())
    except Exception as e:
        print(f"[Daemon] 处理错误: {e}", flush=True)
        try:
            conn.send(f'ERROR: {e}'.encode())
        except:
            pass
    finally:
        conn.close()


def cleanup():
    """清理资源"""
    print("[Daemon] 清理资源...", flush=True)
    global _server_socket
    if _server_socket:
        _server_socket.close()
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)


def run_daemon():
    """运行守护进程"""
    global _server_socket

    # 清理旧的 socket
    if os.path.exists(SOCKET_PATH):
        os.unlink(SOCKET_PATH)

    # 预加载模型（启动时就加载好）
    print("[Daemon] 初始化 Piper TTS...", flush=True)
    get_piper_voice()

    # 创建 Unix Socket
    _server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    _server_socket.bind(SOCKET_PATH)
    _server_socket.listen(5)
    print(f"[Daemon] 监听 {SOCKET_PATH}", flush=True)
    print("[Daemon] 守护进程已就绪，等待请求...", flush=True)

    # 注册清理函数
    atexit.register(cleanup)

    # 信号处理
    def signal_handler(sig, frame):
        print("\n[Daemon] 收到退出信号", flush=True)
        cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 主循环
    while True:
        try:
            conn, _ = _server_socket.accept()
            handle_client(conn)
        except Exception as e:
            print(f"[Daemon] 接受连接错误: {e}", flush=True)


if __name__ == "__main__":
    run_daemon()
