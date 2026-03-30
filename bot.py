import os
import time
from google import genai

def generate_prediction():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: API Key tidak ditemukan!"

    # Inisialisasi klien yang paling stabil
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    
    # Menggunakan model 2.5 Flash terbaru sesuai daftar dari API Key Anda
    target_model = 'gemini-2.5-flash'
    
    prompt_text = """
    [SYSTEM LOGIC V3.1 ACTIVE]
    Tugas: Lakukan Deep Research & Prediksi Presisi untuk pertandingan tenis ATP/Challenger hari ini.
    Gunakan format output MANDATORY:
    1. Ringkasan Temuan Kunci (Servis, Adaptasi Lapangan)
    2. Tabel Probabilitas & Handicap
    3. Prediksi Skor Set & Keyakinan (%)
    """

    try:
        response = client.models.generate_content(
            model=target_model,
            contents=prompt_text
        )
        return response.text
    except Exception as e:
        return f"GAGAL: {str(e)}"

if __name__ == "__main__":
    print("--- Memulai Sesi Analisis Cloud 24 Jam (Gemini 2.5 Flash) ---")
    # Menambahkan jeda kecil agar tidak menabrak limit jika script berjalan beruntun
    time.sleep(3)
    result = generate_prediction()
    print(result)
