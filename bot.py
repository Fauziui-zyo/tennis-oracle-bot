import os
import requests
from google import genai

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
# 1. ENGINE KALIBRASI OTOMATIS (MENCARI POLA MENANG)
# ====================================================
def run_stress_test(client):
    if not client: return "Klien AI tidak siap."
    
    prompt = """
    [SYSTEM ROLE: FORENSIC TENNIS ANALYST]
    TUGAS: Ambil 3 pertandingan ATP atau Challenger yang BARU SAJA SELESAI (dalam 24-48 jam terakhir).
    
    PROSES ANALISA:
    1. Lakukan analisa statistik seolah-olah pertandingan BELUM dimulai.
    2. Berikan angka [CONFIDENCE_HDP: XX%] untuk probabilitas Underdog menang Handicap +1.5 Set.
    3. BANDINGKAN LANGSUNG prediksi Anda dengan SKOR ASLI yang sudah terjadi.
    
    EVALUASI KRITIS:
    - Jika prediksi Anda (Confidence Score) meleset dari hasil asli, jelaskan DATA KUNCI apa yang Anda lewatkan (Misal: Kelelahan, Statistik Servis Kedua, dll).
    - Rumuskan 1 aturan baru yang ketat agar prediksi berikutnya tidak meleset.
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text
    except Exception as e:
        return f"Gagal kalibrasi: {e}"

# ====================================================
# 2. PROMPT OPTIMAL (HANYA AMBIL YANG PASTI)
# ====================================================
def generate_optimized_prediction(client):
    if not client: return "Klien AI tidak siap."
    
    prompt_live = """
    [SYSTEM ROLE: QUANT ORACLE V7.0]
    [STRATEGY: HIGH-PROBABILITY SET HANDICAP +1.5]
    
    TUGAS: Cari 1 pertandingan ATP/Challenger NYATA yang akan berlangsung dalam 12-24 jam ke depan.
    
    SYARAT "SIGNAL GAS" (CONFIDENCE > 85%):
    1. Underdog memiliki persentase "Return Points Won" > 42% dalam 3 laga terakhir.
    2. Favorit memiliki kecenderungan "Double Faults" tinggi atau persentase servis pertama di bawah 60%.
    3. Pertemuan H2H terakhir (jika ada) berakhir dengan set ketat.
    
    JIKA SYARAT TIDAK TERPENUHI ATAU JADWAL TIDAK DITEMUKAN, BERIKAN LABEL [HOLD/NO-BET].
    JANGAN MENGARANG JADWAL PERTANDINGAN.

    FORMAT OUTPUT:
    🎾 MATCH: [Pemain A vs Pemain B]
    📊 KEY DATA: [Fakta statistik utama yang relevan dengan syarat di atas]
    ⚠️ [CONFIDENCE_HDP: XX%]
    💡 SIGNAL: [GAS PASANG BESAR / HOLD (NO-BET)]
    📝 REASON: [Alasan singkat berdasarkan evaluasi data]
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_live)
        return response.text
    except Exception as e:
        return f"Gagal prediksi live: {e}"

if __name__ == "__main__":
    print("--- Menjalankan Kalibrasi & Optimasi V7.0 ---")
    ai_client = get_client()
    
    print("\n[1/2] Memulai Stress Test (Backtest)...")
    stress_test_result = run_stress_test(ai_client)
    
    print("\n[2/2] Memulai Prediksi Optimal Hari Ini...")
    prediction_result = generate_optimized_prediction(ai_client)
    
    final_output = f"=== 🧪 HASIL KALIBRASI MASA LALU ===\n{stress_test_result}\n\n=== 🎯 PREDIKSI OPTIMAL HARI INI ===\n{prediction_result}"
    
    print("\n" + final_output)
    send_telegram(final_output)
    print("\n--- Sesi Selesai ---")
