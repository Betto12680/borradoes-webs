#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Scheduler: Programador Maestro del Sistema Automatizado de Prospección
Ejecuta la secuencia diaria en sus ventanas de horario exactas.
"""

import time
import os
import subprocess
from datetime import datetime

AUTOMATION_DIR = os.path.dirname(os.path.abspath(__file__))

def run_task(script_name):
    script_path = os.path.join(AUTOMATION_DIR, script_name)
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executing {script_name}...")
    try:
        res = subprocess.run(["python3", script_path], check=True, capture_output=True, text=True)
        print(res.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e.stderr}")

def main():
    print("🤖 Master Scheduler Iniciado. Monitoreando horarios diarios...")
    print("• 07:00 AM -> Pipeline 1: Scraping (100 empresas con correo)")
    print("• 08:00 AM -> Pipeline 2: Generación 100 Webs + GitHub Pages")
    print("• 10:00 AM -> Pipeline 3: Envíos Correo en Bloques Anti-Spam")
    print("• 11:00 AM -> Pipeline 4: Seguimiento (Día 3) y Limpieza GitHub (Día 7)")
    
    executed_today = set()

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        today_date = now.strftime("%Y-%m-%d")

        # 07:00 AM
        if current_time == "07:00" and f"p1_{today_date}" not in executed_today:
            run_task("pipeline_1_scraper.py")
            executed_today.add(f"p1_{today_date}")

        # 08:00 AM
        elif current_time == "08:00" and f"p2_{today_date}" not in executed_today:
            run_task("pipeline_2_builder.py")
            executed_today.add(f"p2_{today_date}")

        # 10:00 AM
        elif current_time == "10:00" and f"p3_{today_date}" not in executed_today:
            run_task("pipeline_3_mailer.py")
            executed_today.add(f"p3_{today_date}")

        # 11:00 AM
        elif current_time == "11:00" and f"p4_{today_date}" not in executed_today:
            run_task("pipeline_4_followup_cleaner.py")
            executed_today.add(f"p4_{today_date}")

        time.sleep(30)

if __name__ == "__main__":
    main()
