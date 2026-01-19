# 🤖 AI-Powered Service Assistant (Next Gen Edition)

## 📌 Descrição

Este é um sistema inteligente de triagem de atendimento bancário que utiliza Machine Learning para classificar intenções de usuários e responder de forma automatizada. O projeto foi desenhado para ser escalável, integrando um motor de IA em Python com um ecossistema Full Stack moderno.

## 🛠️ Tecnologias Principais

- **Linguagem:** Python 3.12+
- **IA/ML:** Pandas, NumPy, Scikit-Learn (Multinomial Naive Bayes)
- **Backend:** FastAPI (Python) - Alta performance e tipagem automática.
- **Frontend:** React.js (Vite) ou Next.js - Para uma interface reativa e moderna.
- **Banco de Dados:** MongoDB Atlas (NoSQL) - Flexibilidade para armazenar logs de conversas.
- **Cloud/Auth:** Firebase - Autenticação de usuários e hospedagem estática.

## 🚀 Arquitetura do Sistema

1. **Frontend:** Interface de chat onde o usuário envia mensagens.
2. **API (Backend):** Recebe a mensagem, envia para o modelo de IA e consulta o banco de dados.
3. **Engine de IA:** Script especializado que carrega o modelo treinado (`.pkl`) e retorna a predição.
4. **Database:** Armazena o histórico de interações para futuro re-treinamento do modelo.

## 📈 Roadmap de Escala

- [ ] Protótipo em script Python funcional.
- [ ] Criação da API com FastAPI.
- [ ] Integração com MongoDB para persistência de dados.
- [ ] Desenvolvimento do Frontend e conexão via Axios.
- [ ] Implementação de Segurança com Firebase Auth.
