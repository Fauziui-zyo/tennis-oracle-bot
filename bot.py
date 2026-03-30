import os
import requests
from datetime import datetime
from google import genai
from google.genai import types

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: API Key tidak ditemukan!")
        return None
    return genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Peringatan: Telegram Secret belum diset.")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Membatasi panjang teks agar tidak ditolak Telegram
    if len(message) > 4000:
        message = message[:4000] + "\n\n...[Teks dipotong]"
        
    payload = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Berhasil mengirim laporan ke Telegram!")
        else:
            print(f"Gagal kirim ke Telegram. Status: {response.status_code}")
    except Exception as e:
        print(f"Error koneksi Telegram: {e}")

# ====================================================
# STRATEGI REAL-TIME SEARCH (MENEMBUS BATASAN WAKTU)
# ====================================================
def run_integrated_analysis(client):
    if not client: return "Klien AI tidak siap."
    
    current_date = datetime.now().strftime('%d %B %Y')
    
    prompt = f"""
    [SYSTEM ROLE: REAL-TIME QUANT ANALYST]
    [DATE: {current_date}]
    [STRICT RULE: DILARANG MELAKUKAN SIMULASI. WAJIB GUNAKAN DATA ASLI DARI PENCARIAN WEB]
    
    TUGAS UTAMA ANDA HARI INI:
    1. CARI (SEARCH) di web hasil pertandingan tenis ATP/Challenger yang baru saja selesai dalam 24 jam terakhir.
    2. Lakukan "Blind Backtest": Berikan [CONFIDENCE_HDP: XX%] untuk salah satu laga tersebut seolah belum tahu hasilnya berdasarkan statistik pre-match, lalu bandingkan dengan skor aslinya.
    3. CARI (SEARCH) di web jadwal pertandingan tenis ATP/Challenger untuk hari ini atau besok.
    4. Analisa statistik pemain yang akan bertanding. Temukan 1 "SIGNAL GAS" (CONFIDENCE > 85%) dengan kriteria:
       - Underdog memiliki rekor "Return Points Won" yang kuat.
       - Favorit memiliki kelemahan servis (Double Faults tinggi atau 1st Serve % rendah).
    
    JIKA TIDAK ADA DATA YANG MEMENUHI SYARAT, BERIKAN LABEL [HOLD / NO-BET].
    
    FORMAT OUTPUT (SINGKAT & JELAS):
    === 🧪 REAL-TIME CALIBRATION ===
    [Analisa laga kemarin berdasarkan data pencarian web]
    
    === 🎯 REAL-TIME PREDIKSI PASTI ===
    MATCH: [Nama Pemain A vs Pemain B]
    VULNERABILITY: [Kelemahan lawan berdasarkan data nyata web]
    [CONFIDENCE_HDP: XX%]
    SIGNAL: [GAS PASANG BESAR / HOLD (NO-BET)]
    """

    try:
        # Menjalankan AI dengan fitur Google Search aktif
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}]
            )
        )
        return response.text
    except Exception as e:
        return f"Gagal dalam analisis terintegrasi: {e}"

if __name__ == "__main__":
    print("--- Menjalankan V9.0 (Search Integrated) ---")
    ai_client = get_client()
    
    print("\n[!] Mengakses Google Search untuk mencari data tenis terbaru...")
    full_analysis = run_integrated_analysis(ai_client)
    
    print("\n" + full_analysis)
    send_telegram(full_analysis)
    print("\n--- Sesi Selesai ---")
