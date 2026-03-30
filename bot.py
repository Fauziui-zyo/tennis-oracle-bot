import os
import json
import requests
from datetime import datetime
from google import genai

# ====================================================
# 1. SETUP API & TELEGRAM (KONEKSI CLOUD)
# ====================================================
def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: API Key tidak ditemukan di GitHub Secrets!")
        return None
    # Menggunakan api_version v1 agar stabil dan terhindar dari error 404
    return genai.Client(api_key=api_key, http_options={'api_version': 'v1'})

def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("Peringatan: Telegram Token/Chat ID belum diset. Hasil hanya tampil di log GitHub.")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # Telegram memiliki batas 4096 karakter per pesan. Kita amankan di sini.
    if len(message) > 4000:
        message = message[:4000] + "\n\n...[Pesan dipotong karena limit Telegram]"
        
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Berhasil mengirim laporan ke Telegram Anda!")
        else:
            print(f"Gagal kirim ke Telegram. Status: {response.status_code}")
    except Exception as e:
        print(f"Error koneksi Telegram: {e}")

# ====================================================
# 2. MESIN KALIBRASI (BELAJAR DARI PERTANDINGAN LEWAT)
# ====================================================
def calibrate_system(client):
    if not client: return "Klien AI tidak siap."
    
    # AREA TRIAL & ERROR ANDA:
    # Ganti nama pemain di bawah ini dengan pertandingan yang baru saja selesai kemarin.
    test_cases = [
        {"p1": "Carlos Alcaraz", "p2": "Grigor Dimitrov", "event": "ATP Miami"},
        {"p1": "Jannik Sinner", "p2": "Daniil Medvedev", "event": "ATP Miami"}
    ]
    
    report = "=== 🧪 SESI KALIBRASI BACKTEST ===\n"
    
    for match in test_cases:
        prompt = f"""
        [SIMULATION MODE: BLIND BACKTEST]
        Pertandingan: {match['p1']} vs {match['p2']} ({match['event']}).
        
        TUGAS ANDA: 
        1. Lakukan analisa statistik (Servis, H2H, Lapangan) seolah-olah laga ini BELUM dimulai.
        2. Wajib berikan angka [CONFIDENCE_HDP: XX%] untuk probabilitas Pemain Underdog mencuri minimal 1 set (Handicap +1.5).
        3. VERIFIKASI: Setelah Anda membuat prediksi, bandingkan dengan SKOR ASLI yang sudah terjadi di dunia nyata.
        4. Kesimpulan Kalibrasi: Apakah tebakan [CONFIDENCE_HDP] Anda akurat menebak hasil aslinya?
        """
        
        try:
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
            report += f"\n🎾 **{match['p1']} vs {match['p2']}**\n{response.text}\n"
            report += "-" * 30 + "\n"
        except Exception as e:
            report += f"Gagal memproses kalibrasi {match['p1']}: {e}\n"
            
    return report

# ====================================================
# 3. MESIN PREDIKSI LIVE (UNTUK TARUHAN HARI INI)
# ====================================================
def generate_live_prediction(client):
    if not client: return "Klien AI tidak siap."
    
    prompt_live = """
    [LIVE MODE: ANALISA PERTANDINGAN HARI INI]
    Tugas: Lakukan analisa mendalam untuk 1 pertandingan ATP/Challenger teratas yang akan berlangsung HARI INI.
    Fokus utama: Mencari VALUE/Keuntungan paling aman pada market "Set Handicap +1.5".
    
    FORMAT OUTPUT MANDATORY:
    🎾 PERTANDINGAN HARI INI: [Pemain A vs Pemain B]
    📊 TEMUAN KUNCI: [Analisa Servis, Kelelahan, dan H2H]
    📈 KONDISI LAPANGAN: [Dampak Kelembapan/Kecepatan pada pukulan]
    ⚠️ [CONFIDENCE_HDP: XX%] (Wajib isi dengan angka probabilitas)
    🏆 PREDIKSI SKOR SET: [X-X]
    💡 REKOMENDASI FINAL: [GAS PASANG BESAR / HINDARI LAGA INI]
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_live)
        return response.text
    except Exception as e:
        return f"Gagal memproses prediksi live: {e}"

# ====================================================
# 4. EKSEKUSI UTAMA (JALAN OTOMATIS 24 JAM)
# ====================================================
if __name__ == "__main__":
    waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"--- Memulai Sesi Quant v5.5 ({waktu_sekarang}) ---")
    
    ai_client = get_client()
    
    print("\n[1/3] Menjalankan Kalibrasi Historis...")
    hasil_kalibrasi = calibrate_system(ai_client)
    print("Selesai.")
    
    print("\n[2/3] Menjalankan Prediksi Hari Ini...")
    hasil_live = generate_live_prediction(ai_client)
    print("Selesai.")
    
    print("\n[3/3] Menyusun Laporan dan Mengirim ke Telegram...")
    final_report = f"{hasil_kalibrasi}\n\n=== 🎯 PREDIKSI LIVE HARI INI ===\n{hasil_live}"
    
    # Cetak di log GitHub agar Anda bisa melihatnya jika Telegram bermasalah
    print("\n" + final_report)
    
    # Kirim langsung ke HP Anda
    send_telegram(final_report)
    print("\n--- Sesi Selesai dengan Sukses ---")
