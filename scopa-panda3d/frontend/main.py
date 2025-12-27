#!/usr/bin/env python3
import socket
import threading
import sys

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectButton import DirectButton
from direct.gui.OnscreenText import OnscreenText


class Frontend(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.title = OnscreenText(text="Scopa - Panda3D Frontend", pos=(0, 0.9), scale=0.07)
        self.status = OnscreenText(text="Status: disconnected", pos=(0, -0.9), scale=0.05)

        self.btn_start = DirectButton(text="Start", scale=0.08, pos=(-0.6, 0, 0.7), command=self.send_cmd, extraArgs=["START"])
        self.btn_play = DirectButton(text="Play Random", scale=0.08, pos=(0, 0, 0.7), command=self.send_cmd, extraArgs=["PLAY CARD1"])
        self.btn_ping = DirectButton(text="Ping Backend", scale=0.06, pos=(0.6, 0, 0.7), command=self.send_cmd, extraArgs=["HELLO"])

        self.sock = None
        self.latest_status = "disconnected"
        self.lock = threading.Lock()

        # Periodic task to update on-screen status from threads
        self.taskMgr.add(self.update_task, "update_task")

        # Connect in background
        threading.Thread(target=self.connect_backend, daemon=True).start()

    def update_task(self, task):
        with self.lock:
            self.status.setText("Status: " + self.latest_status)
        return task.cont

    def set_status(self, text):
        with self.lock:
            self.latest_status = text

    def connect_backend(self):
        try:
            self.sock = socket.create_connection(("127.0.0.1", 5000), timeout=5)
            self.set_status("connected")
            threading.Thread(target=self.read_loop, daemon=True).start()
        except Exception as e:
            self.set_status("connect failed: " + str(e))

    def read_loop(self):
        try:
            f = self.sock.makefile('r')
            for line in f:
                self.set_status("backend: " + line.strip())
        except Exception as e:
            self.set_status("read error: " + str(e))
        finally:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None
            self.set_status("connection closed")

    def send_cmd(self, cmd):
        if not self.sock:
            self.set_status("not connected")
            return
        try:
            self.sock.sendall((cmd + "\n").encode("utf-8"))
        except Exception as e:
            self.set_status("send failed: " + str(e))


if __name__ == "__main__":
    app = Frontend()
    app.run()
