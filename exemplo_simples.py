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

    return(response)

mensagem = "Gere um texto curto explicando o que é RAG e como ele funciona."

response = gerar_textos(mensagem)

print(response)