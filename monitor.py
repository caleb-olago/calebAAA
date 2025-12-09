import psutil
import time  
import socket
import platform
import distro
import datetime
import os

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

        print()
        print(" Informations sur le système")
        print()
        print("Heure de démarrage :", bootime_datetime.strftime("%d-%m-%Y %H:%M:%S"))
        print("Nombre d'utilisateurs connectés :", len(Nb_users))
        print("Nom d'hôte :", hotsname)
        print("Système d'exploitation :", system)
        print("Distribution :", distrobution)
        print("Adresse IP :", ip)

        print()
        print(" I Liste des processus en cours avec leur consommation CPU (%)")
        print()

        cpu_list = []
        for p in psutil.process_iter(['name', 'cpu_percent']):
            info = p.info
            info['cpu_percent'] = info['cpu_percent'] or 0
            cpu_list.append(info)
            print(info)

        print()
        print(" I Liste des processus en cours avec leur consommation RAM (%)")
        print()

        ram_list = []
        for p in psutil.process_iter(['name', 'memory_percent']):
            info = p.info
            info['memory_percent'] = info['memory_percent'] or 0
            ram_list.append(info)
            print(info)

        print()
        print("  TOP 3 des processus les plus gourmands en CPU (%)")
        print()

        top_cpu = sorted(cpu_list, key=lambda x: x['cpu_percent'], reverse=True)[:3]
        for proc in top_cpu:
            print(f"{proc['name']} : {proc['cpu_percent']} % CPU")

        print()
        print("  TOP 3 des processus les plus gourmands en RAM (%)")
        print()

        top_ram = sorted(ram_list, key=lambda x: x['memory_percent'], reverse=True)[:3]
        for proc in top_ram:
            print(f"{proc['name']} : {proc['memory_percent']:.2f} % RAM")

        folder_path = "/home"

        print()
        print(" Analyse simple des fichiers dans :", folder_path)
        print()

        extensions = [".txt", ".py", ".pdf", ".jpg"]
        counts = {ext: 0 for ext in extensions}

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                _, ext = os.path.splitext(filename.lower())
                if ext in counts:
                    counts[ext] += 1

            all = sum(counts.values())

            print("Total fichiers trouvés :", all)
            print()

            for ext in extensions:
                print(f"{ext} : {counts[ext]} fichier(s)")
        else:
            print("⚠️  Chemin non valide.")

        time.sleep(15)

infosystem()
