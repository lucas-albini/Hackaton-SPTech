import streamlit as st
import boto3

client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

def chamada_api(prompt):

    response = client.converse(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=prompt,
        inferenceConfig={"maxTokens":2048,"stopSequences":["\n\nHuman:"],"temperature":1,"topP":1},
        additionalModelRequestFields={"top_k":250}
    )

    response_text = response["output"]["message"]["content"][0]["text"]

    return(response_text)

def gerar_textos(mensagem):

    st.session_state.mensagem = ""
    st.session_state.imagem = ""


    with text_spinner_placeholder:
        with st.spinner("Por favor aguarde enquanto sua mensagem está sendo gerada..."):

            system_prompt = """
            Você é um assistente de IA que está ajudando um usuário a gerar textos.

            Você receberá uma solicitação de um usuário e deverá responder a essa solicitação.

            A solicitação do usuário estará dentro das tags <text></text>.
            """

            input_prompt = f"{system_prompt} \n\nHuman: <text>{mensagem}</text> \n\nAssistant:"

            conversation = [
                {
                    "role": "user",
                    "content": [{"text": input_prompt}],
                }
            ]

            response = chamada_api(conversation)

            st.session_state.mensagem = (response)

st.set_page_config(page_title="Hackaton-SPTech")

if "mensagem" not in st.session_state:
    st.session_state.mensagem = ""

st.title("Hackaton-SPTech") 
st.markdown("Exemplo de aplicação de IA para geração de textos.")

text_spinner_placeholder = st.empty()

with st.form('message_form'):
  text = st.text_area('Escreva sua mensagem:', '')
  submitted = st.form_submit_button('Gerar texto')
  if submitted:
    gerar_textos(text)


if st.session_state.mensagem:
    st.markdown("""---""")
    st.text_area(label="Resposta:", value=st.session_state.mensagem, height=500)

    
image_spinner_placeholder = st.empty()