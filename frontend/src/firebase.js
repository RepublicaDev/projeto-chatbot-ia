import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCimsnCbPeyQXPXa3ic3-jybCsEnOvBGPs",
  authDomain: "ia-chatbot-554d7.firebaseapp.com",
  projectId: "ia-chatbot-554d7",
  storageBucket: "ia-chatbot-554d7.firebasestorage.app",
  messagingSenderId: "1059952726024",
  appId: "1:1059952726024:web:44a423605b620dd8d341bd",
  measurementId: "G-8ZMSENKMC2"
};

// Inicializa o Firebase
const app = initializeApp(firebaseConfig);

// Exporta o Auth para usarmos no login
export const auth = getAuth(app);