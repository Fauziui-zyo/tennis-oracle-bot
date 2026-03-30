import os
import google.generativeai as genai

# Setup API Key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("ERROR: GEMINI_API_KEY tidak ditemukan di Secret GitHub!")

genai.configure(api_key=api_key)

def generate_prediction():
    # MENGGUNAKAN NAMA MODEL LENGKAP UNTUK MENGHINDARI 404
    # Kita arahkan ke model 'gemini-1.5-flash-latest' yang paling stabil
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "max_output_tokens": 2048,
        }
    )

    learning_context = "Analisis Terakhir: Fokus pada tren servis pertama 48 jam terakhir dan adaptasi kelembapan pesisir."
    
    prompt = f"""
    [SYSTEM LOGIC V3.1 ACTIVE]
    Konteks: {learning_context}
    
    Tugas: Lakukan Deep Research & Prediksi Presisi untuk pertandingan tenis ATP/Challenger hari ini.
    Gunakan format output MANDATORY:
    1. Ringkasan Temuan Kunci (Servis, Adaptasi Lapangan)
    2. Tabel Probabilitas & Handicap
    3. Simulasi Worst-Case
    4. Prediksi Skor Set & Keyakinan (%)
    """
    
    try:
        # Melakukan generate content dengan penanganan error yang lebih baik
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            return "AI mengembalikan respon kosong. Cek kuota API Anda."
    except Exception as e:
        return f"GAGAL MEMANGGIL AI: {str(e)}"

if __name__ == "__main__":
    print("--- Memulai Sesi Analisis Cloud 24 Jam (V1.5 Flash Stabil) ---")
    result = generate_prediction()
    print(result)
