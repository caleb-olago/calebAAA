import psutil
import time  
import socket
import platform
import distro
import datetime

def infosystem():
    while True:

        print("\033c", end="")
        
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_frequency = psutil.cpu_freq().current
        cpu_usage = psutil.cpu_percent(interval=1)

        print()
        print(" Informations sur le  CPU")
        print()
        print(f"Nombre de cœurs    : {cpu_cores}")
        print(f"Fréquence actuelle : {cpu_frequency:.2f} MHz")
        print(f"Utilisation CPU    : {cpu_usage:.1f} %")

