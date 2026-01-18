import os
import datetime
import joblib
import firebase_admin
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from firebase_admin import credentials, auth
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# 1. CARREGAR CONFIGURAÇÕES
load_dotenv()

# 2. CONFIGURAÇÃO FIREBASE
firebase_creds = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "token_uri": "https://oauth2.googleapis.com/token",
}

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred)

app = FastAPI()

# 3. MIDDLEWARE CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. CONFIGURAÇÃO MONGODB
MONGO_URL = os.getenv("MONGODB_URL") 
client = AsyncIOMotorClient(MONGO_URL)
db = client.chatbot_db
collection = db.historico_mensagens

# 5. CARREGAR IA
modelo = joblib.load('models/modelo_ia.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

class MensagemUsuario(BaseModel):
    texto: str

@app.post("/chat")
async def responder_chat(mensagem: MensagemUsuario, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token ausente")
    
    try:
        token = authorization.split("Bearer ")[1]
        decoded_token = auth.verify_id_token(token)
        usuario_id = decoded_token['uid']
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    # 6. IA PROCESSA A MENSAGEM
    # Transforma o texto do usuário usando o vectorizer
    texto_vet = vectorizer.transform([mensagem.texto.lower()])
    # Predição
    categoria = str(modelo.predict(texto_vet)[0])
    
    print(f"DEBUG - Msg: {mensagem.texto} | Categoria: {categoria}")

    respostas = {
        'Pagamento': 'Para pagar, use o menu "Pagamentos" no app ou escaneie o código de barras com sua câmera.',
        'Suporte': 'Nosso suporte técnico está online. Se o app travar, tente limpar o cache ou reinstalar.',
        'Reclamação': 'Lamentamos muito o transtorno. Registramos seu feedback e um analista irá revisar seu caso.',
        'Consulta': 'Seu saldo e extrato detalhado podem ser visualizados na tela principal do aplicativo.'
    }
    
    # Busca a resposta baseada na categoria (case-sensitive com o dicionário acima)
    reply = respostas.get(categoria, "Entendi sua dúvida, mas ainda estou aprendendo sobre isso. Pode detalhar melhor?")

    # 7. SALVAR NO MONGODB
    log_interacao = {
        "usuario_id": usuario_id,
        "usuario_msg": mensagem.texto,
        "ia_intent": categoria,
        "ia_reply": reply,
        "data": datetime.datetime.utcnow()
    }
    await collection.insert_one(log_interacao)

    return {"intent": categoria, "reply": reply}

@app.get("/")
def home():
    return {"status": "Servidor e IA Online"}