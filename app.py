import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from flask import Flask, request, render_template
from datetime import date, datetime
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    today = date.today().strftime('%Y-%m-%d')
    if request.method == 'POST':
        subdir = request.form['subdir']
        selected_date = request.form['date']
        log_file = os.path.join('/var/log/network-monitor/', subdir, selected_date + '.log')
        if os.path.exists(log_file):
            # 打开日志文件
            with open(log_file, 'r') as f:
                # 读取日志文件中的所有内容
                content = f.read()

            # 按行分割内容
            lines = content.split('\n')

            # 创建列表来存储数据
            times = []
            txs = []
            rxs = []

            # 遍历每一行
            for line in lines:
                # 跳过空行
                if not line:
                    continue

                # 按空格分割行
                parts = line.split(' ')

                # 获取时间、流入流量和流出流量
                time, tx, rx = parts[0], float(parts[1]), float(parts[2])

                # 将数据添加到列表中
                times.append(datetime.strptime(time, '%H:%M:%S'))
                txs.append(tx / (1024 * 1024))
                rxs.append(rx / (1024 * 1024))

            # 设置图表的大小
            plt.figure(figsize=(12, 6))
            # 绘制折线图
            plt.plot(times, txs, label='transmit')
            plt.plot(times, rxs, label='receive')
            plt.legend()
            # 设置X轴的范围和刻度标签
            plt.xlim([times[0], times[-1]])
            plt.xticks(rotation=45)
            plt.ylabel('MBps/s')
            # 添加以下代码
            hours = mdates.HourLocator(interval=1)
            h_fmt = mdates.DateFormatter('%H:%M:%S')
            ax = plt.gca()
            ax.xaxis.set_major_locator(hours)
            ax.xaxis.set_major_formatter(h_fmt)
            # 设置X轴的范围为一天24小时
            ax.set_xlim([datetime(1900, 1, 1, 0, 0, 0), datetime(1900, 1, 2, 0, 0, 0)])
            img = BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('index.html', subdir=subdir, date=selected_date, plot_url=plot_url)
        else:
            return render_template('index.html', error=f'No log file found for {subdir} on {selected_date}')
    return render_template('index.html', subdir='dumpserver', date=today)

if __name__ == '__main__':
    app.run()

