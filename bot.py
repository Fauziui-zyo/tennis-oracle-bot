import os
import json
import requests
from datetime import datetime
from google import genai

# --- 1. KONFIGURASI DATABASE MEMORI ---
MEMORY_FILE = "database_memori.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as file:
            return json.load(file)
    return {"total_prediksi": 0, "riwayat": []}

def save_memory(data):
    with open(MEMORY_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# --- 2. INTEGRASI TELEGRAM ---
def send_telegram(message):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Peringatan: Telegram Token/Chat ID tidak ditemukan di GitHub Secrets.")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# --- 3. OTAK ANALISA & PREDIKSI (GEMINI 2.5 FLASH) ---
def generate_prediction(memory_data):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: API Key tidak ditemukan!", 0
        
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    
    # Memberikan AI konteks memori agar ia belajar
    total_laga = memory_data.get("total_prediksi", 0)
    
    prompt_text = f"""
    [SYSTEM ROLE: ELITE TENNIS QUANTITATIVE ANALYST V5.0]
    [DATA HISTORIS BOT: Anda telah melakukan {total_laga} prediksi sejauh ini.]
    
    Tugas: Lakukan analisa mendalam untuk 1 pertandingan ATP/Challenger teratas hari ini.
    Fokus utama: Mencari VALUE pada market "Set Handicap +1.5".
    
    Instruksi Wajib:
    1. Anda HARUS memberikan persentase keyakinan.
    2. Format wajib untuk persentase Handicap adalah persis seperti ini: [CONFIDENCE_HDP: XX%]
    
    FORMAT OUTPUT MANDATORY:
    🎾 PERTANDINGAN: [Pemain A vs Pemain B]
    📊 TEMUAN KUNCI (Backtest & Dinamika Servis): [Analisa Anda]
    📈 KONDISI LAPANGAN: [Analisa Kelembapan/Angin]
    ⚠️ [CONFIDENCE_HDP: XX%]
    🏆 PREDIKSI SKOR SET: [X-X]
    """

    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_text)
        prediction_text = response.text
        
        # Ekstrak Angka Confidence untuk Filter
        confidence_score = 0
        if "[CONFIDENCE_HDP:" in prediction_text:
            try:
                # Mengambil angka dari teks [CONFIDENCE_HDP: 88%]
                score_str = prediction_text.split("[CONFIDENCE_HDP:")[1].split("%")[0].strip()
                confidence_score = int(score_str)
            except:
                confidence_score = 0
                
        return prediction_text, confidence_score
    except Exception as e:
        return f"GAGAL MEMANGGIL AI: {str(e)}", 0

# --- 4. FILTER THRESHOLD (TRIAL & ERROR) ---
def evaluate_signal(confidence_score):
    # Di sinilah titik Trial & Error Anda. Saat ini diset 85%.
    THRESHOLD = 85 
    
    if confidence_score == 0:
        return "⚠️ Gagal membaca persentase keyakinan. Pasang taruhan dengan hati-hati."
    elif confidence_score >= THRESHOLD:
        return f"🔥 [SIGNAL PASTI] Skor {confidence_score}% memenuhi ambang batas {THRESHOLD}%. HIGH VALUE BET!"
    else:
        return f"🛑 [NO BET / HOLD] Skor {confidence_score}% di bawah batas aman {THRESHOLD}%. RISIKO TINGGI."

# --- 5. EKSEKUSI UTAMA ---
if __name__ == "__main__":
    print("--- Memulai Sesi V5.0 (Learning & Threshold Mode) ---")
    
    # 1. Baca Ingatan
    memori = load_memory()
    
    # 2. Buat Prediksi
    raw_prediction, conf_score = generate_prediction(memori)
    
    # 3. Evaluasi Sinyal (Apakah layak dipasang?)
    signal_status = evaluate_signal(conf_score)
    
    # 4. Susun Laporan Akhir
    final_report = f"{raw_prediction}\n\n--- KESIMPULAN SISTEM ---\n{signal_status}"
    print(final_report)
    
    # 5. Kirim ke Telegram
    send_telegram(final_report)
    
    # 6. Simpan ke Memori (Belajar)
    memori["total_prediksi"] += 1
    memori["riwayat"].append({
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confidence": conf_score,
        "signal": "GAS" if conf_score >= 85 else "HOLD"
    })
    save_memory(memori)
    print("Sesi selesai. Memori telah diperbarui.")
