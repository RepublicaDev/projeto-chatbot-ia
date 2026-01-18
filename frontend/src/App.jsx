import React, { useState, useEffect, useRef } from "react";
import "./App.css";
import axios from "axios";
import { auth } from "./firebase";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  signOut,
} from "firebase/auth";
import { Send, Bot, User, Sparkles, LogOut, Lock } from "lucide-react";

function App() {
  const [user, setUser] = useState(null);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { text: "Olá! Sou sua IA. Como posso ajudar?", isBot: true },
  ]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    console.log("chamei o firebase aqui", user);
    const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
      setUser(currentUser);
      console.log("Auth state changed, user:", currentUser);
    });

    return () => unsubscribe();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAuth = async (type) => {
    try {
      if (type === "login")
        await signInWithEmailAndPassword(auth, email, password);
      else await createUserWithEmailAndPassword(auth, email, password);
    } catch (error) {
      alert("Erro: " + error.message);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || !user) return;

    // 1. Limpa o input e adiciona a mensagem do usuário
    const userMsg = { text: input, isBot: false };
    setMessages((prev) => [...prev, userMsg]);
    const currentInput = input; // Salva o input atual
    setInput("");

    try {
      const token = await user.getIdToken();
      const response = await axios.post(
        "https://projeto-chatbot-ia.onrender.com/chat",
        { texto: currentInput }, // Envia o texto correto
        { headers: { Authorization: `Bearer ${token}` } },
      );

      // 2. Adiciona a resposta NOVA vinda do servidor
      const botMsg = {
        text: response.data.reply,
        isBot: true,
        intent: response.data.intent,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Erro na API:", error);
      setMessages((prev) => [
        ...prev,
        { text: "Ops, tive um erro técnico aqui.", isBot: true },
      ]);
    }
  };

  // 1. TELA DE LOGIN
  if (!user) {
    return (
      <div className="auth-container">
        <div className="auth-card">
          <Lock size={40} color="#6366f1" style={{ margin: "0 auto" }} />
          <h2>Acesso Restrito</h2>
          <input
            type="email"
            placeholder="E-mail"
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Senha"
            onChange={(e) => setPassword(e.target.value)}
          />
          <div className="auth-buttons">
            <button onClick={() => handleAuth("login")}>Entrar</button>
            <button className="secondary" onClick={() => handleAuth("signup")}>
              Cadastrar
            </button>
          </div>
        </div>
      </div>
    );
  } else {
    // 2. TELA DO CHAT COMPLETA
    return (
      <div className="chat-container">
        <header className="chat-header">
          <div
            className="header-info"
            style={{ display: "flex", alignItems: "center", gap: "10px" }}
          >
            <Sparkles size={20} color="#818cf8" />
            <h2 style={{ margin: 0, fontSize: "1.2rem" }}>AI Assistant</h2>
          </div>
          <button onClick={() => signOut(auth)} className="logout-btn">
            <LogOut size={18} />
          </button>
        </header>

        <div className="messages-list">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`message-wrapper ${msg.isBot ? "bot" : "user"}`}
            >
              <div className="icon">
                {msg.isBot ? <Bot size={18} /> : <User size={18} />}
              </div>
              <div className="message-bubble">
                {msg.text}
                {msg.intent && <span className="intent-tag">{msg.intent}</span>}
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Como posso ajudar?"
          />
          <button onClick={handleSend} className="send-button">
            <Send size={20} />
          </button>
        </div>
      </div>
    );
  }
}

export default App;
