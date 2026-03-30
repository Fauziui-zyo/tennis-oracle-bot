import os
import google.generativeai as genai

# Konfigurasi API Key dari Secret GitHub
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di environment variables!")

genai.configure(api_key=api_key)

# MENGGUNAKAN MODEL TERBARU (1.5 Flash - Gratis & Stabil)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_learning_data():
    # Simulasi data untuk Trial & Error
    return "Analisis Terakhir: Prediksi Shevchenko 2-0 benar. Navone 2-1 benar. Fokus pada adaptasi angin pesisir."

def generate_prediction():
    learning_context = get_learning_data()
    
    # Prompt v3.1 yang sudah dioptimalkan
    prompt = f"""
    [SYSTEM UPDATE: LOGIC V3.1 ACTIVE]
    Konteks Pembelajaran: {learning_context}
    
    Tugas: Berikan analisa Deep Research dan Prediksi Presisi untuk pertandingan tenis hari ini.
    Fokus pada:
    1. Dinamika Servis (Weight 40%)
    2. Kondisi Lapangan & Biomekanik (Weight 25%)
    3. Filter Reality Check (Weight 20%)
    4. Psikologi (Weight 15%)
    
    Berikan output dalam format Ringkasan Temuan, Tabel Probabilitas, dan Prediksi Skor Akhir.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan saat memanggil AI: {str(e)}"

if __name__ == "__main__":
    print("--- Memulai Sesi Analisis Cloud 24 Jam (V1.5 Flash) ---")
    result = generate_prediction()
    print(result)
