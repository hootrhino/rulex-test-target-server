import time
import tkinter as tk
import socket
import json
import threading
import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 6002


class UDPReceiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((UDP_IP, UDP_PORT))

        self.root = tk.Tk()
        self.root.title("UDP Server")
        self.root.geometry("700x400")
        self.root.config(bg="black")

        self.room_label = tk.Label(self.root, text="实验室工B-407", font=("Arial", 40))
        self.room_label.config(bg="black", fg="red")
        self.room_label.pack()

        self.time_label = tk.Label(self.root, text="当前时间:", font=("Arial", 30))
        self.time_label.config(bg="black", fg="green")
        self.time_label.pack()

        self.tag_label = tk.Label(self.root, text="传感器:", font=("Arial", 40))
        self.tag_label.config(bg="black", fg="green")
        self.tag_label.pack()

        self.humi_label = tk.Label(self.root, text="湿度:0", font=("Arial", 40))
        self.humi_label.config(bg="black", fg="green")
        self.humi_label.pack()

        self.temp_label = tk.Label(self.root, text="温度", font=("Arial", 40))
        self.temp_label.config(bg="black", fg="green")
        self.temp_label.pack()

    def start(self):
        threading.Thread(target=self.update_time_label).start()
        threading.Thread(target=self.receive_data).start()
        self.root.mainloop()

    def receive_data(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(1024)
                json_data = json.loads(data.decode())
                tag = json_data.get("tag", "d1")
                temp = json_data.get("temp", 0)
                humi = json_data.get("hum", 0)
                self.root.after(
                    0, self.update_labels, f"设备:{tag}", f"温度:{temp}℃", f"湿度:{humi}%"
                )
            except json.JSONDecodeError:
                print("Invalid JSON data received.")

    def update_labels(self, tag, temp, humi):
        self.tag_label.config(text=str(tag))
        self.temp_label.config(text=str(temp))
        self.humi_label.config(text=str(humi))

    def update_time_label(self):
        while True:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.root.after(0, self.time_label.config(text=f"当前时间:{current_time}"))
            time.sleep(1)


if __name__ == "__main__":
    receiver = UDPReceiver()
    receiver.start()
