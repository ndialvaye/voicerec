# app.py

import streamlit as st
import speech_recognition as sr
import os

# Titre de l'application
st.title("🎤 Speech Recognition App (Streamlit Cloud)")

# Choix de l'API
api_choice = st.selectbox(
    "Choisissez votre API de reconnaissance vocale :",
    ("Google Web Speech API", "Sphinx (Offline)")
)

# Choix de la langue
language_choice = st.selectbox(
    "Choisissez votre langue :",
    ("en-US", "fr-FR", "es-ES", "de-DE", "it-IT")
)

# Upload du fichier audio
uploaded_file = st.file_uploader("Uploadez un fichier audio (.wav ou .flac)", type=["wav", "flac"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")

    recognizer = sr.Recognizer()

    with sr.AudioFile(uploaded_file) as source:
        st.info("🔍 Analyse de l'audio...")
        audio = recognizer.record(source)
    
    try:
        # Reconnaissance vocale
        if api_choice == "Google Web Speech API":
            text = recognizer.recognize_google(audio, language=language_choice)
        elif api_choice == "Sphinx (Offline)":
            text = recognizer.recognize_sphinx(audio, language=language_choice)

        st.success("✅ Texte reconnu :")
        st.write(text)

        # Sauvegarde du texte
        if st.button("💾 Sauvegarder la transcription"):
            with open("transcription.txt", "w", encoding="utf-8") as f:
                f.write(text)
            st.success("Transcription sauvegardée dans le fichier 'transcription.txt'.")

    except sr.UnknownValueError:
        st.error("❗️ Impossible de comprendre l'audio. Veuillez essayer avec un autre fichier.")
    except sr.RequestError as e:
        st.error(f"❗️Erreur de service : {e}")

else:
    st.warning("⏳ Veuillez uploader un fichier audio pour commencer.")
