import streamlit as st
import boto3
import json
import base64
from io import BytesIO

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def chamada_api(prompt):

    request = json.dumps({
        "text_prompts": [{"text":prompt,"weight":1}],
        "cfg_scale": 10,
        "steps": 50,
        "seed": 0,
        "width": 512,
        "height": 512,
        "samples": 1,
    })

    response = client.invoke_model(modelId="stability.stable-diffusion-xl-v1", body=request)

    # Decode the response body.
    model_response = json.loads(response["body"].read())

    # Extract the image data.
    base64_image_data = model_response["artifacts"][0]["base64"]

    imagem_bites = BytesIO(base64.b64decode(base64_image_data))

    return(imagem_bites)

def gerar_imagens(mensagem):
    with image_spinner_placeholder:
        with st.spinner("Por favor aguarde enquanto sua imagem está sendo gerada..."):

            response = chamada_api(mensagem)
            st.session_state.imagem = (response)

st.set_page_config(page_title="Hackaton-SPTech")

if "imagem" not in st.session_state:
    st.session_state.imagem = ""

st.title("Hackaton-SPTech") 
st.markdown("Exemplo de aplicação de IA para geração de imagens.")

image_spinner_placeholder = st.empty()

if not st.session_state.imagem:
    with st.form('image_form'):
        text = st.text_area('Descreva sua imagem:', '')
        submitted = st.form_submit_button('Gerar imagem')
        if submitted:
            gerar_imagens(text)
            st.image(st.session_state.imagem)
else:
    with st.form('image_form'):
        text = st.text_area('Descreva sua imagem:', '')
        submitted = st.form_submit_button('Gerar imagem')
        if submitted:
            gerar_imagens(text)
            st.image(st.session_state.imagem)

image_spinner_placeholder = st.empty()