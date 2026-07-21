#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob

BASE_DIR = '/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web'

BULLET_HTML = '<div class="pulse-bullet-dot"><span class="dot"></span></div>'

BULLET_CSS = """
        /* Viñetas Animadas (Punticos con Pulso) */
        .pulse-bullet-dot { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; margin-bottom: 16px; }
        .pulse-bullet-dot .dot { width: 10px; height: 10px; border-radius: 50%; background-color: var(--secondary, #38bdf8); position: relative; box-shadow: 0 0 10px var(--secondary, #38bdf8); }
        .pulse-bullet-dot .dot::after { content: ''; position: absolute; top: -4px; left: -4px; right: -4px; bottom: -4px; border-radius: 50%; border: 2px solid var(--secondary, #38bdf8); animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite; }
        @keyframes pulse-ring { 0% { transform: scale(0.5); opacity: 0.9; } 100% { transform: scale(1.8); opacity: 0; } }
"""

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. Inject CSS if not present
    if 'pulse-bullet-dot' not in content:
        content = content.replace('</style>', BULLET_CSS + '\n    </style>')

    # 2. Replace any <div class="srv-icon">...</div> or <div class="srv-icon-box">...</div> or <div class="card-icon">...</div> with BULLET_HTML
    content = re.sub(r'<div class="(?:srv-icon|srv-icon-box|card-icon)">[\s\S]*?</div>', BULLET_HTML, content)

    # 3. If .srv-icon CSS exists, remove or neutralize the 64px box styling so it doesn't leave leftover boxes
    content = re.sub(r'\.srv-icon\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.srv-icon-box\s*\{[^}]*\}', '', content)
    content = re.sub(r'\.card-icon\s*\{[^}]*\}', '', content)

    if content != orig:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = glob.glob(os.path.join(BASE_DIR, '**/index.html'), recursive=True)
    count = 0
    for f in html_files:
        if process_file(f):
            count += 1
            print(f"✔ Viñeta animada aplicada en: {os.path.relpath(f, BASE_DIR)}")
    print(f"\nTotal procesados: {count} de {len(html_files)}")

if __name__ == "__main__":
    main()
