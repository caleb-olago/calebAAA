import psutil
import time
import socket
import platform
import distro
import datetime
import os

TEMPLATE_PATH = "template.html"
OUTPUT_PATH = "dashboard.html"

def infosystem():
    while True:
        # --- CPU ---
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_frequency = psutil.cpu_freq().current
        cpu_usage = psutil.cpu_percent(interval=1)

        # --- RAM ---
        mem = psutil.virtual_memory()
        usedram = mem.used / (1024**3)
        allram = mem.total / (1024**3)
        percentram = mem.percent

        # --- Système ---
        hostname = socket.gethostname()
        system = platform.system()
        if system == "Linux":
            distribution = distro.name()
        else:
            distribution = "inconnue"

        boottime_datetime = datetime.datetime.fromtimestamp(psutil.boot_time())
        nb_users = psutil.users()
        ip = socket.gethostbyname(hostname)

        # --- Processus CPU ---
        cpu_list = []
        for p in psutil.process_iter(['name', 'cpu_percent']):
            info = p.info
            info['cpu_percent'] = info['cpu_percent'] or 0
            cpu_list.append(info)

        top_cpu = sorted(cpu_list, key=lambda x: x['cpu_percent'], reverse=True)[:3]

        top_cpu_rows = ""
        for proc in top_cpu:
            name = proc.get('name') or "N/A"
            cpu_p = proc.get('cpu_percent') or 0
            top_cpu_rows += f"<tr><td>{name}</td><td>{cpu_p}</td></tr>\n"

        # --- Processus RAM ---
        ram_list = []
        for p in psutil.process_iter(['name', 'memory_percent']):
            info = p.info
            info['memory_percent'] = info['memory_percent'] or 0
            ram_list.append(info)

        top_ram = sorted(ram_list, key=lambda x: x['memory_percent'], reverse=True)[:3]

        top_ram_rows = ""
        for proc in top_ram:
            name = proc.get('name') or "N/A"
            mem_p = proc.get('memory_percent') or 0
            top_ram_rows += f"<tr><td>{name}</td><td>{mem_p:.2f}</td></tr>\n"

        # --- Analyse des fichiers ---
        folder_path = "/home"
        extensions = [".txt", ".py", ".pdf", ".jpg"]
        counts = {ext: 0 for ext in extensions}

        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                _, ext = os.path.splitext(filename.lower())
                if ext in counts:
                    counts[ext] += 1
            total_files = sum(counts.values())
        else:
            total_files = 0

        files_list_html = ""
        for ext, count in counts.items():
            files_list_html += f"<li>{ext} : <strong>{count}</strong> fichier(s)</li>\n"

        # --- Lecture du template HTML ---
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            template = f.read()

        # --- Remplacement des placeholders ---
        html = template
        html = html.replace("{{CPU_CORES}}", str(cpu_cores))
        html = html.replace("{{CPU_FREQ}}", f"{cpu_frequency:.2f}")
        html = html.replace("{{CPU_USAGE}}", f"{cpu_usage:.1f}")

        html = html.replace("{{RAM_USED}}", f"{usedram:.2f}")
        html = html.replace("{{RAM_TOTAL}}", f"{allram:.2f}")
        html = html.replace("{{RAM_PERCENT}}", f"{percentram:.1f}")

        html = html.replace("{{BOOT_TIME}}", boottime_datetime.strftime("%d-%m-%Y %H:%M:%S"))
        html = html.replace("{{NB_USERS}}", str(len(nb_users)))
        html = html.replace("{{HOSTNAME}}", hostname)
        html = html.replace("{{OS}}", system)
        html = html.replace("{{DISTRO}}", distribution)
        html = html.replace("{{IP_ADDR}}", ip)

        html = html.replace("{{TOP_CPU_ROWS}}", top_cpu_rows)
        html = html.replace("{{TOP_RAM_ROWS}}", top_ram_rows)

        html = html.replace("{{FOLDER_PATH}}", folder_path)
        html = html.replace("{{FILES_TOTAL}}", str(total_files))
        html = html.replace("{{FILES_LIST}}", files_list_html)

        # --- Écriture du fichier final ---
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(html)

        print("Dashboard mis à jour :", OUTPUT_PATH)

        time.sleep(15)

# appel direct, simple comme tu veux
infosystem()
