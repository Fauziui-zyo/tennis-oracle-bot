import os
from google import genai

def generate_prediction():
    # Mengambil API Key dari GitHub Secret
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "ERROR: API Key tidak ditemukan!"

    # Inisialisasi Client Baru (SDK 2026)
    client = genai.Client(api_key=api_key)
    
    prompt_text = """
    [SYSTEM LOGIC V3.1 ACTIVE]
    Tugas: Lakukan Deep Research & Prediksi Presisi untuk pertandingan tenis ATP/Challenger hari ini.
    Gunakan format output MANDATORY:
    1. Ringkasan Temuan Kunci (Servis, Adaptasi Lapangan)
    2. Tabel Probabilitas & Handicap
    3. Simulasi Worst-Case
    4. Prediksi Skor Set & Keyakinan (%)
    """

    try:
        # Memanggil model gemini-1.5-flash dengan SDK terbaru
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt_text
        )
        return response.text
    except Exception as e:
        return f"GAGAL TOTAL: {str(e)}"

if __name__ == "__main__":
    print("--- Memulai Sesi Analisis Cloud 24 Jam (SDK 2.0 - 2026) ---")
    result = generate_prediction()
    print(result)
