import os
import requests
from google import genai

def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: API Key tidak ditemukan!")
        return None
    # Menggunakan api_version v1 agar stabil
    return genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Peringatan: Telegram Secret belum diset.")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Batasi panjang pesan agar tidak ditolak Telegram (Limit 4096 karakter)
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
# 1. LIVE DATA SCANNER (MARET 2026 FOCUS)
# ====================================================
def run_realtime_calibration(client):
    if not client: return "Klien AI tidak siap."
    
    # Sinkronisasi Waktu Paksa
    current_date = "31 Maret 2026"
    prompt = f"""
    [SYSTEM ROLE: DATA SCIENTIST & TENNIS ANALYST]
    [CURRENT DATE: {current_date}]
    
    TUGAS: Ambil 2 pertandingan ATP/Challenger yang baru saja SELESAI di Miami Open atau turnamen Maret 2026 lainnya.
    
    PROSES:
    1. Bedah statistik servis & return pre-match.
    2. Berikan [CONFIDENCE_HDP: XX%] untuk probabilitas Underdog menang Handicap +1.5 Set.
    3. Verifikasi dengan skor asli 2026.
    4. Jika [CONFIDENCE_HDP] > 85% tapi kalah, temukan "Anomali Data" (Cedera/Cuaca/Mental).
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text
    except Exception as e:
        return f"Gagal kalibrasi: {e}"

# ====================================================
# 2. OPTIMIZED ORACLE (THE 85% THRESHOLD)
# ====================================================
def generate_pasti_prediction(client):
    if not client: return "Klien AI tidak siap."
    
    current_date = "31 Maret 2026"
    prompt_live = f"""
    [SYSTEM ROLE: QUANT ORACLE V8.0]
    [DATE: {current_date}]
    [STRATEGY: SET HANDICAP +1.5 VALUE HUNTER]
    
    Cari 1 pertandingan NYATA untuk hari ini atau besok (31 Maret / 1 April 2026).
    
    KRITERIA "PASTI MENANG" (CONFIDENCE > 85%):
    - Underdog Return Points Won > 42%.
    - Favorit 1st Serve % < 60% di laga terakhir.
    - Kondisi Lapangan mendukung gaya Underdog.

    JIKA JADWAL ATAU DATA TIDAK VALID, BERIKAN LABEL [HOLD/NO-BET].

    FORMAT OUTPUT:
    MATCH: [Pemain A vs Pemain B]
    VULNERABILITY: [Kelemahan fatal pemain favorit]
    [CONFIDENCE_HDP: XX%]
    SIGNAL: [GAS / HOLD]
    VALUE REASONING: [Kenapa data ini valid?]
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_live)
        return response.text
    except Exception as e:
        return f"Gagal prediksi live: {e}"

if __name__ == "__main__":
    print("--- Menjalankan V8.0 (Sync 2026) ---")
    ai_client = get_client()
    
    print("\n[1/2] Memulai Kalibrasi Real-Time...")
    calibration = run_realtime_calibration(ai_client)
    
    print("\n[2/2] Memulai Prediksi Pasti...")
    prediction = generate_pasti_prediction(ai_client)
    
    final_report = f"=== 🧪 KALIBRASI MARET 2026 ===\n{calibration}\n\n=== 🎯 PREDIKSI PASTI ===\n{prediction}"
    
    print("\n" + final_report)
    send_telegram(final_report)
    print("\n--- Sesi Selesai ---")
