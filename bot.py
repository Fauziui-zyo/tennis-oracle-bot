import os
import pandas as pd
import google.generativeai as genai

# Setup Gemini (Otak Analisis)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def get_learning_data():
    # Simulasi memuat data hasil kemarin (Trial & Error)
    # Di v4.0, Anda bisa mengganti ini dengan API Tenis gratis
    return "Hasil kemarin: Moriya menang 2-0, sesuai prediksi. Navone menang 2-1, melesat dari 2-0."

def generate_prediction():
    learning_context = get_learning_data()
    prompt = f"""
    Analisis v3.1 sebelumnya: {learning_context}
    Tugas: Berikan prediksi parlay aman untuk pertandingan hari ini.
    Gunakan bobot dinamis: Jika kelembapan >70%, naikkan bobot fisik.
    Output: Ringkasan, Probabilitas, dan Skor Set.
    """
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("--- Memulai Sesi Analisis Cloud 24 Jam ---")
    prediction = generate_prediction()
    print(prediction)
    # Hasil ini akan muncul di log GitHub Actions Anda tiap sesi
