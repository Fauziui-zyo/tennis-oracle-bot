import os
from google import genai

def generate_prediction():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: API Key tidak ditemukan!"

    # Memaksa penggunaan API v1 yang paling stabil, bukan v1beta
    client = genai.Client(api_key=api_key, http_options={'api_version': 'v1'})
    
    # Kita coba menggunakan generasi terbaru Gemini 2.0 Flash
    target_model = 'gemini-2.0-flash'
    
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
        # SISTEM AUTO-DEBUG: Jika model tidak ditemukan, cetak semua model yang tersedia!
        error_msg = f"GAGAL memanggil {target_model}. Error: {str(e)}\n"
        error_msg += "\n--- DAFTAR MODEL YANG TERSEDIA UNTUK API KEY ANDA ---\n"
        try:
            for m in client.models.list():
                error_msg += f"- {m.name}\n"
            error_msg += "---------------------------------------------------\n"
            error_msg += "Solusi: Salin salah satu nama model di atas (yang ada kata 'flash' atau 'pro') dan ganti variabel 'target_model' di kode Anda."
        except Exception as list_error:
            error_msg += f"Gagal mengambil daftar model: {str(list_error)}"
            
        return error_msg

if __name__ == "__main__":
    print("--- Memulai Sesi Analisis Cloud 24 Jam (Auto-Debug Mode) ---")
    result = generate_prediction()
    print(result)
