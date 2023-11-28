import tkinter as tk
import requests
import tkinter.font as tkFont

# 映射JSON字段和注释的字典
field_mapping = {
    "device_id": "设备ID",
    "recv_time": "接收时间",
    "bat_voltage": "电池电压",
    "longitude": "经度",
    "latitude": "纬度",
    "air_height": "空气高度",
    "water_temp": "水温",
    "salinity": "盐度",
    "dissolved_oxygen": "溶解氧",
    "ph_value": "pH值",
    "wind_speed": "风速",
    "wind_direction": "风向",
    "air_temp": "空气温度",
    "air_pressure": "大气压力",
    "air_humidity": "空气湿度",
    "noise": "噪声",
    "wave_height": "海浪高度",
    "mean_wave_period": "平均波周期",
    "peak_wave_period": "峰值波周期",
    "mean_wave_direction": "平均波方向",
}


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("海洋水质监控浮球数据监控器")

        self.create_widgets()

        # 设置定时器，每隔3秒调用一次get_data方法
        self.root.after(3000, self.get_data_periodically)

    def create_widgets(self):
        # 创建标签和文本框
        self.url_label = tk.Label(self.root, text="URL:")
        self.url_entry = tk.Entry(
            self.root,
            textvariable=tk.StringVar(
                value="#"
            ),
        )
        self.result_text = tk.Text(
            self.root,
            height=20,
            width=40,
            foreground="#bed742",
            background="#121a2a",
            font=tkFont.Font(size=20, weight="bold"),
        )

        # 创建按钮
        self.get_data_button = tk.Button(
            self.root, text="Get Data", command=self.get_data
        )

        # 安排标签和控件的位置
        self.url_label.grid(row=0, column=0, sticky=tk.E)
        self.url_entry.grid(row=0, column=1, columnspan=2)
        self.get_data_button.grid(row=0, column=3)
        self.result_text.grid(row=2, column=0, columnspan=4)

    def get_data(self):
        # 从URL获取JSON数据
        url = self.url_entry.get()
        try:
            response = requests.get(url)
            data = response.json()

            # 清空文本框
            self.result_text.delete(1.0, tk.END)

            # 遍历JSON数据，显示在文本框中
            for key, value in data.items():
                # 获取对应的注释
                label_text = f"{field_mapping.get(key, key)}: {value}"
                self.result_text.insert(tk.END, label_text + "\n")

        except Exception as e:
            # 处理异常情况，比如无效的URL或JSON格式错误
            error_message = f"Error: {str(e)}"
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, error_message)

    def get_data_periodically(self):
        self.get_data()
        self.root.after(2000, self.get_data_periodically)


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
