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

        mem = psutil.virtual_memory()
        usedram = mem.used / (1024**3)
        allram = mem.total / (1024**3)
        percentram = mem.percent

        print()
        print(" Informations sur la RAM ")
        print()
        print(f"RAM utilisée   : {usedram:.2f} GB")
        print(f"RAM totale     : {allram:.2f} GB")
        print(f"Utilisation RAM : {percentram:.1f} %")

        hotsname = socket.gethostname()
        system = platform.system()
        if system == "Linux":
            distrobution = distro.name()
        else:
            distrobution = "inconnue"

        bootime_datetime = datetime.datetime.fromtimestamp(psutil.boot_time())
        Nb_users = psutil.users()
        ip = socket.gethostbyname(hotsname)
