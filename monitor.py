import psutil
import socket
import platform
import distro
import datetime
import os

# Chemins
TEMPLATE_PATH = "template.html"                     
CSS_PATH = "template.css"                           
OUTPUT_HTML = "/var/www/html/dashboard.html"        
OUTPUT_CSS = "/var/www/html/template.css"          

def infosystem():

    # CPU ---
    cpu_cores = psutil.cpu_count(logical=True)
    cpu_frequency = psutil.cpu_freq().current
    cpu_usage = psutil.cpu_percent(interval=1)

    # RAM ---
    mem = psutil.virtual_memory()
    usedram = mem.used / (1024**3)
    allram = mem.total / (1024**3)
    percentram = mem.percent

    # système ---
    hostname = socket.gethostname()
    system = platform.system()
    distribution = distro.name() if system == "Linux" else "inconnue"
    boottime_datetime = datetime.datetime.fromtimestamp(psutil.boot_time())
    nb_users = psutil.users()
    ip = socket.gethostbyname(hostname)

    # Top CPU
    cpu_list = []
    for p in psutil.process_iter(['name', 'cpu_percent']):
        try:
            info = p.info
            info['cpu_percent'] = info['cpu_percent'] or 0
            cpu_list.append(info)
        except:
            continue

    top_cpu = sorted(cpu_list, key=lambda x: x['cpu_percent'], reverse=True)[:3]
    top_cpu_rows = ""
    for proc in top_cpu:
        name = proc.get('name') or "N/A"
        cpu_p = proc.get('cpu_percent') or 0
        top_cpu_rows += f"<tr><td>{name}</td><td>{cpu_p}</td></tr>\n"

    # Top RAM
    ram_list = []
    for p in psutil.process_iter(['name', 'memory_percent']):
        try:
            info = p.info
            info['memory_percent'] = info['memory_percent'] or 0
            ram_list.append(info)
        except:
            continue

    top_ram = sorted(ram_list, key=lambda x: x['memory_percent'], reverse=True)[:3]
    top_ram_rows = ""
    for proc in top_ram:
        name = proc.get('name') or "N/A"
        mem_p = proc.get('memory_percent') or 0
        top_ram_rows += f"<tr><td>{name}</td><td>{mem_p:.2f}</td></tr>\n"

    # fichiers ---
    folder_path = "/home"
    extensions = [".txt", ".py", ".pdf", ".jpg"]
    counts = {ext: 0 for ext in extensions}

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            _, ext = os.path.splitext(filename.lower())
            if ext in counts:
                counts[ext] += 1

    total_files = sum(counts.values())

    files_list_html = ""
    for ext, count in counts.items():
        files_list_html += f"<li>{ext} : <strong>{count}</strong> fichier(s)</li>\n"

    # chargement template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

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

    # ecriture du dashboard
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    # Ccopier le CSS dans apache
    os.system(f"sudo cp {CSS_PATH} {OUTPUT_CSS}")

    print("Dashboard généré dans /var/www/html/dashboard.html")

infosystem()
