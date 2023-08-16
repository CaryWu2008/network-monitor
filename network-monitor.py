import time
import os
from datetime import datetime

def monitor_network(interface, interval, log_dir):
    rx_bytes, tx_bytes = 0, 0
    rx_rates, tx_rates = [], []
    while True:
        with open(f'/sys/class/net/{interface}/statistics/rx_bytes', 'r') as f:
            rx = int(f.read())
        with open(f'/sys/class/net/{interface}/statistics/tx_bytes', 'r') as f:
            tx = int(f.read())
        if rx_bytes and tx_bytes:
            rx_rate = rx - rx_bytes
            tx_rate = tx - tx_bytes
            rx_rates.append(rx_rate)
            tx_rates.append(tx_rate)
            if len(rx_rates) == interval:
                avg_rx_rate = sum(rx_rates) / interval
                avg_tx_rate = sum(tx_rates) / interval
                timestamp = datetime.now().strftime('%H:%M:%S')
                log_file = os.path.join(log_dir, datetime.now().strftime('%Y-%m-%d') + '.log')
                with open(log_file, 'a') as f:
                    f.write(f'{timestamp} {avg_tx_rate} {avg_rx_rate}\n')
                rx_rates, tx_rates = [], []
        rx_bytes, tx_bytes = rx, tx
        time.sleep(1)

monitor_network('team0', 30, '/var/log/network-monitor/')

