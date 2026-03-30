import os
import json
import requests
from datetime import datetime
from google import genai
from google.genai import types

# ====================================================
# KONFIGURASI DATABASE LOKAL
# ====================================================
DB_FILE = "parlay_raksasa.json"
TARGET_MATCHES = 30

def load_parlay_list():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_parlay_list(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ====================================================
# INTEGRASI TELEGRAM (SILENT MODE)
# ====================================================
def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    # Hanya kirim jika ada isi pesan (tidak kosong)
    if not token or not chat_id or not message.strip(): 
        return
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": message})

# ====================================================
# KONEKSI AI
# ====================================================
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key: 
        return None
    return genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

# ====================================================
# MESIN PENCARI & PENYARING (REAL-TIME)
# ====================================================
def find_top_matches(client):
    google_search_tool = types.Tool(google_search=types.GoogleSearch())
    
    prompt = f"""
    [SYSTEM ROLE: ELITE QUANT COLLECTOR]
    [DATE: {datetime.now().strftime('%d %B %Y')}]

    TUGAS:
    Gunakan Google Search untuk mencari maksimal 3 pertandingan tenis ATP/Challenger NYATA yang akan dimainkan dalam 24-48 jam ke depan.
    HANYA pilih yang memenuhi syarat "Set Handicap +1.5" dengan keyakinan > 85%:
    - Underdog Return Points Won > 42%
    - Favorit 1st Serve < 60%

    FORMAT OUTPUT HARUS SANGAT KETAT (HANYA POIN-POIN INI, TANPA TEKS LAIN/BASA-BASI AWALAN/AKHIRAN):
    - [Pemain Underdog] +1.5 vs [Pemain Favorit] | Confidence: XX% | [1 kalimat alasan statistik spesifik]
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=types.GenerateContentConfig(tools=[google_search_tool])
        )
        return response.text
    except Exception as e:
        print(f"Error AI: {e}")
        return ""

# ====================================================
# EKSEKUSI UTAMA (AKUMULASI)
# ====================================================
if __name__ == "__main__":
    print("--- Menjalankan V10.1 (Silent Accumulator) ---")
    client = get_client()
    
    if not client:
        print("API Key hilang.")
        exit()
        
    parlay_list = load_parlay_list()
    
    # Jika target 30 laga sudah tercapai
    if len(parlay_list) >= TARGET_MATCHES:
        full_list = "\n".join(parlay_list)
        send_telegram(f"🔥 TIKET PARLAY 30 LAGA SELESAI 🔥\n\n{full_list}")
        print("Target 30 laga tercapai. Tiket final dikirim.")
        # Hapus list untuk memulai siklus 30 laga yang baru berikutnya
        save_parlay_list([]) 
        exit()

    # Jika belum 30, cari laga baru
    new_matches_text = find_top_matches(client)
    
    if new_matches_text and "-" in new_matches_text:
        # Filter ketat: Hanya ambil teks yang dimulai dengan tanda strip (poin-poin)
        new_lines = [line.strip() for line in new_matches_text.split('\n') if line.strip().startswith('-')]
        
        valid_new_lines = []
        if new_lines:
            # Simpan laga baru ke database lokal (pastikan tidak duplikat)
            for line in new_lines:
                if len(parlay_list) < TARGET_MATCHES and line not in parlay_list:
                    parlay_list.append(line)
                    valid_new_lines.append(line)
            
            save_parlay_list(parlay_list)
            
            # Kirim MURNI HANYA poin-poin prediksi terbaru ke Telegram
            if valid_new_lines:
                telegram_message = "\n".join(valid_new_lines)
                send_telegram(telegram_message)
            
            print(f"Ditemukan {len(valid_new_lines)} laga baru. Total tersimpan: {len(parlay_list)}/{TARGET_MATCHES}")
        else:
            print("Tidak ada laga yang lolos filter ketat hari ini.")
    else:
        print("Tidak ada laga yang lolos filter ketat hari ini.")
