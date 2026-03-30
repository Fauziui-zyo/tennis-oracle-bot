import os
import requests
from datetime import datetime
from google import genai

# ====================================================
# 1. SETUP API & TELEGRAM (ANTI-ERROR 400)
# ====================================================
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
    
    if len(message) > 4000:
        message = message[:4000] + "\n\n...[Teks dipotong]"
        
    # MENGHAPUS parse_mode="Markdown" UNTUK MENCEGAH ERROR 400
    payload = {"chat_id": chat_id, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Berhasil mengirim ke Telegram!")
        else:
            print(f"Gagal kirim ke Telegram. Status: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error koneksi Telegram: {e}")

# ====================================================
# 2. MESIN KALIBRASI (TRIAL & ERROR MASA LALU)
# ====================================================
def calibrate_system(client):
    if not client: return ""
    
    # SILAKAN GANTI NAMA PEMAIN DI BAWAH INI DENGAN PERTANDINGAN KEMARIN
    test_cases = [
        {"p1": "Gael Monfils", "p2": "Dusan Lajovic", "event": "ATP Miami 2026"},
        {"p1": "Ben Shelton", "p2": "Lorenzo Musetti", "event": "ATP Miami 2026"}
    ]
    
    report = "=== 🧪 SESI KALIBRASI BACKTEST ===\n"
    
    for match in test_cases:
        prompt = f"""
        [SIMULATION MODE: BLIND BACKTEST]
        Pertandingan: {match['p1']} vs {match['p2']} ({match['event']}).
        
        TUGAS: Lakukan analisa statistik (Servis & H2H) seolah laga ini BELUM dimulai.
        Wajib berikan [CONFIDENCE_HDP: XX%] untuk probabilitas Underdog mencuri minimal 1 set.
        """
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            report += f"\n🎾 {match['p1']} vs {match['p2']}\n{response.text}\n"
            report += "-" * 20 + "\n"
        except Exception as e:
            report += f"Gagal kalibrasi: {e}\n"
            
    return report

# ====================================================
# 3. MESIN PREDIKSI LIVE (V6.0 PRECISION FILTER)
# ====================================================
def generate_live_prediction(client):
    if not client: return ""
    
    tanggal_sekarang = datetime.now().strftime('%Y-%m-%d')
    
    prompt_live = f"""
    [SYSTEM ROLE: TENNIS QUANTITATIVE ANALYST V6.0]
    [WAKTU SEKARANG: {tanggal_sekarang} (Maret 2026)]
    [STRICT RULE: DILARANG MENGHALUSINASI JADWAL. GUNAKAN JADWAL ATP/CHALLENGER NYATA HARI INI]

    Tugas: Analisa 1 pertandingan ATP/Challenger NYATA yang berlangsung hari ini. Jika tidak ada jadwal yang Anda yakini 100% nyata, tulis "TIDAK ADA JADWAL VALID HARI INI".
    
    FILTER KEAMANAN (WAJIB):
    1. PENALTI MOMENTUM: Kurangi akurasi jika pemain favorit kelelahan/kalah set pertama di laga sebelumnya.
    2. SURFACE CHECK: Jika lapangan CLAY, utamakan pemain ulet dengan Return Points Won tinggi.
    3. H2H CHECK: Underdog hanya boleh dipegang (Handicap +1.5) jika pernah merepotkan unggulan dalam pertemuan sebelumnya.

    WAJIB OUTPUT DALAM FORMAT SINGKAT INI:
    🎾 MATCH HARI INI: [Nama Pemain A vs Pemain B]
    📊 STATS: [1 Kalimat fakta servis/return yang paling krusial]
    📉 MOMENTUM: [Kondisi fisik/kelelahan]
    ⚠️ [CONFIDENCE_HDP: XX%] (Isi dengan angka prediksi Anda)
    🏆 PREDIKSI SKOR: [X-X]
    💡 REKOMENDASI: [GAS PASANG / HOLD (NO-BET)]
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_live)
        return response.text
    except Exception as e:
        return f"Gagal memproses prediksi live: {e}"

# ====================================================
# 4. EKSEKUSI UTAMA
# ====================================================
if __name__ == "__main__":
    print("--- Memulai Sesi Quant v6.0 ---")
    
    ai_client = get_client()
    
    hasil_kalibrasi = calibrate_system(ai_client)
    hasil_live = generate_live_prediction(ai_client)
    
    final_report = f"{hasil_kalibrasi}\n\n=== 🎯 PREDIKSI LIVE HARI INI ===\n{hasil_live}"
    
    print(final_report)
    send_telegram(final_report)
