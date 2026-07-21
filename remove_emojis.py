#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob

BASE_DIR = '/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web'

# Modern Clean SVG replacements
SVG_WA = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-right:6px;"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>'
SVG_WA_FLOAT = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/></svg>'
SVG_STAR = '<svg width="16" height="16" viewBox="0 0 24 24" fill="#fbbf24" stroke="#fbbf24" stroke-width="2" style="display:inline-block; vertical-align:middle; margin-right:4px;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
SVG_ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle; margin-left:4px;"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'

# Generic SVG Icon for service cards
SVG_SERVICE_DEFAULT = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
SVG_STETHOSCOPE = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4.8 2.3A.3.3 0 0 0 4.5 2.6V10a5 5 0 0 0 10 0V2.6a.3.3 0 0 0-.3-.3h-1.4a.3.3 0 0 0-.3.3V10a3 3 0 0 1-6 0V2.6a.3.3 0 0 0-.3-.3H4.8z"/><path d="M9.5 15a4.5 4.5 0 0 0 4.5 4.5h1a2.5 2.5 0 0 0 2.5-2.5v-1.5"/><circle cx="17.5" cy="13.5" r="2"/></svg>'
SVG_MICROSCOPE = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0-14 0"/><path d="M9 14l2-2"/><path d="M12 11l3-3"/><path d="M15 8l2-2"/></svg>'
SVG_SHIELD = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
SVG_DIAMOND = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 12L2 9z"/></svg>'
SVG_ACTIVITY = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'

EMOJI_REPLACEMENTS = {
    '💬': SVG_WA,
    '⭐': SVG_STAR,
    '⭐': SVG_STAR,
    '👉': SVG_ARROW,
    '↗': SVG_ARROW,
    '✨': '',
    '💎': SVG_DIAMOND,
    '🩺': SVG_STETHOSCOPE,
    '🔬': SVG_MICROSCOPE,
    '🛡️': SVG_SHIELD,
    '🧠': SVG_ACTIVITY,
    '🧘': SVG_ACTIVITY,
    '🏃': SVG_ACTIVITY,
    '🗣️': SVG_STETHOSCOPE,
    '🫁': SVG_STETHOSCOPE,
    '🧸': SVG_STETHOSCOPE,
    '📊': SVG_MICROSCOPE,
    '📋': SVG_STETHOSCOPE,
    '🤝': SVG_STETHOSCOPE,
    '🏥': SVG_SHIELD,
    '🫀': SVG_ACTIVITY,
    '⚡': SVG_ACTIVITY,
}

# Regex to catch any remaining unicode emoji ranges
EMOJI_REGEX = re.compile(r'[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF\u2600-\u26FF\u2700-\u27BF]')

def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Replace float WhatsApp button content specifically
    content = re.sub(r'class="wa-float-btn"[^>]*>\s*(?:<div[^>]*></div>)?\s*💬', r'class="wa-float-btn" target="_blank" aria-label="WhatsApp Directo">' + SVG_WA_FLOAT, content)
    content = re.sub(r'class="wa-float"[^>]*>\s*💬', r'class="wa-float" target="_blank" aria-label="WhatsApp Directo">' + SVG_WA_FLOAT, content)

    # 2. Replace known emojis with SVGs
    for emoji, svg in EMOJI_REPLACEMENTS.items():
        content = content.replace(emoji, svg)

    # 3. Strip any remaining emojis
    content = EMOJI_REGEX.sub('', content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    html_files = glob.glob(os.path.join(BASE_DIR, '**/index.html'), recursive=True)
    cleaned_count = 0
    for file_path in html_files:
        if process_html_file(file_path):
            cleaned_count += 1
            print(f"✔ Emojis reemplazados por vectores en: {os.path.relpath(file_path, BASE_DIR)}")

    print(f"\nTotal de archivos actualizados: {cleaned_count} de {len(html_files)}")

if __name__ == "__main__":
    main()
