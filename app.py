import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONFIGURACIÓN GOOGLE SHEETS ---
# Reemplaza esto con el ID de tu hoja de cálculo compartida
SPREADSHEET_ID = "1RT55pZ9W0hZ_8GtV4Dv1HTT5MI-b2qAnnuMhxPtDpZY"
SHEET_NAME = "Hoja 1"

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

# --- INTERFAZ DE LA APP ---
st.title("Registro CEPREPUC - Asistencia Interactiva")

# Lista de alumnos (puedes reemplazar por la real desde otra hoja)
nombres = [cell.value for cell in sheet.col_values(2)][1:]  # Evita la cabecera

nombre = st.selectbox("Selecciona tu nombre", nombres)
col1, col2 = st.columns(2)
with col1:
    col = st.selectbox("Columna donde te ubicas", list(range(1, 7)))
with col2:
    fila = st.selectbox("Fila donde te ubicas", list(range(1, 9)))

repaso = st.radio("¿Repasaste la clase pasada?", ["Sí", "No"])
comprende = st.radio("¿Estás comprendiendo el tema actual?", ["Sí", "Más o menos", "No"])
estado = st.radio("Estado actual", ["En clase", "Salgo un momento"])

if st.button("Registrar"):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registros = sheet.get_all_records()

    # Verificar si ya se registró hoy
    ya_registro = any(r["Nombre"] == nombre and r["FechaHora"].startswith(datetime.now().strftime("%Y-%m-%d")) for r in registros)

    if ya_registro:
        st.warning("Ya registraste tu asistencia hoy.")
    else:
        sheet.append_row([fecha_hora, nombre, col, fila, repaso, comprende, estado])
        st.success("✅ Registro guardado correctamente.")