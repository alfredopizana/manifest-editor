import streamlit as st
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

st.title("App Distribuidos")

archivo = st.file_uploader("Sube un archivo JSON", type=["json"])

if archivo is not None:
    contenido = json.load(archivo)

    # Diccionario con valores a modificar
    opciones = {
        "Type": contenido["myASG"]["Type"],
        "VPCZoneIdentifier": contenido["myASG"]["Properties"]["VPCZoneIdentifier"],
        "Ref": contenido["myASG"]["Properties"]["LaunchTemplate"]["LaunchTemplateId"]["Ref"],
        "myLaunchTemplate": contenido["myASG"]["Properties"]["LaunchTemplate"]["Version"]["Fn::GetAtt"][0],
        "LatestVersionNumber": contenido["myASG"]["Properties"]["LaunchTemplate"]["Version"]["Fn::GetAtt"][1],
        "MaxSize": contenido["myASG"]["Properties"]["MaxSize"],
        "MinSize": contenido["myASG"]["Properties"]["MinSize"]
    }

    # Guardar en session_state para persistencia
    if "valores" not in st.session_state or st.session_state.valores.keys() != opciones.keys():
        st.session_state.valores = opciones.copy()

    # Dropdown para seleccionar clave
    seleccion = st.selectbox("Selecciona una opción:", list(st.session_state.valores.keys()))
    nuevo_valor = st.text_input("Modifica el valor:", value=str(st.session_state.valores[seleccion]))

    # Botón para actualizar el JSON
    if st.button("Actualizar"):
        st.session_state.valores[seleccion] = nuevo_valor
        st.success(f"Valor actualizado: {seleccion} → {nuevo_valor}")

    # Aplicar cambios al JSON original
    contenido["myASG"]["Type"] = st.session_state.valores["Type"]
    contenido["myASG"]["Properties"]["VPCZoneIdentifier"] = st.session_state.valores["VPCZoneIdentifier"]
    contenido["myASG"]["Properties"]["LaunchTemplate"]["LaunchTemplateId"]["Ref"] = st.session_state.valores["Ref"]
    contenido["myASG"]["Properties"]["LaunchTemplate"]["Version"]["Fn::GetAtt"][0] = st.session_state.valores["myLaunchTemplate"]
    contenido["myASG"]["Properties"]["LaunchTemplate"]["Version"]["Fn::GetAtt"][1] = st.session_state.valores["LatestVersionNumber"]
    contenido["myASG"]["Properties"]["MaxSize"] = st.session_state.valores["MaxSize"]
    contenido["myASG"]["Properties"]["MinSize"] = st.session_state.valores["MinSize"]

    # Mostrar el JSON actualizado
    st.subheader("JSON Actualizado:")
    st.json(contenido)  # Mostrar el JSON actualizado en formato visual legible

    # Convertir JSON a string con formato
    json_modificado = json.dumps(contenido, indent=4)

    st.download_button(
        label="Descargar JSON Modificado",
        data=json_modificado,
        file_name="json_actualizado.json",
        mime="application/json"
    )

    if st.button("Enviar a Slack"):
        payload = {
            "text": "Aquí está el JSON actualizado:\n\n" + json_modificado
        }
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)

        if response.status_code == 200:
            st.success("Enviado")
        else:
            st.error(f"Msg error: {response.status_code}")