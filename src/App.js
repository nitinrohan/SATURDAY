import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Sparkles, Heart, Brain, LogOut } from "lucide-react";
import ChatMessage from "./components/ChatMessage";
import TypingIndicator from "./components/TypingIndicator";
import Header from "./components/Header";
import FloatingParticles from "./components/FloatingParticles";
import Login from "./components/Login";

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
`;

const ChatContainer = styled(motion.div)`
  flex: 1;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  margin-bottom: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

const InputContainer = styled(motion.div)`
  display: flex;
  gap: 10px;
  align-items: center;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  padding: 15px 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
`;

const Input = styled.input`
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: white;
  font-size: 16px;
  font-weight: 400;

  &::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }
`;

const SendButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;

  &:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const WelcomeMessage = styled(motion.div)`
  text-align: center;
  color: white;
  margin-bottom: 20px;

  h2 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
    background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  p {
    font-size: 1.1rem;
    opacity: 0.9;
    line-height: 1.6;
  }
`;

const FeaturesGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 30px;
`;

const FeatureCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;

  h3 {
    font-size: 1.2rem;
    margin-bottom: 10px;
    font-weight: 600;
  }

  p {
    opacity: 0.8;
    font-size: 0.9rem;
  }
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  // Backend URL configuration
  const BACKEND_URL =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
      ? "http://localhost:10000"
      : window.location.origin;

  const emotionEmojis = {
    sadness: "💙",
    joy: "😄",
    anger: "🔥",
    fear: "😱",
    love: "❤️",
    gratitude: "🙏",
    confusion: "🤔",
    curiosity: "🔍",
    neutral: "🙂",
    positive: "🌟",
    negative: "😔",
    surprise: "😲",
    relief: "😌",
    guilt: "🌼",
    grief: "🖤",
    pride: "🏆",
    excitement: "🎉",
    nervousness: "💪",
    disgust: "😖",
    admiration: "🌟",
    jealousy: "💚",
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue.trim();
    setInputValue("");
    setIsLoading(true);

    // Add user message
    const newUserMessage = {
      id: Date.now(),
      text: userMessage,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newUserMessage]);

    // Show typing indicator
    setIsTyping(true);

    try {
      const response = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
          message: userMessage,
          session_id: sessionId 
        }),
      });

      const data = await response.json();

      // Remove typing indicator
      setIsTyping(false);

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        text: data.bot_response,
        sender: "bot",
        emotion: data.predicted_emotion,
        emoji: emotionEmojis[data.predicted_emotion] || "🤖",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Error:", error);
      setIsTyping(false);

      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting. Please try again.",
        sender: "bot",
        emotion: "neutral",
        emoji: "😔",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  const handleLogin = (credentials) => {
    // Simulate successful login
    setUser({ email: credentials.email, name: credentials.email.split('@')[0] });
    setIsLoggedIn(true);
    setSessionId(`session_${Date.now()}`);
  };

  const handleGuestLogin = () => {
    setUser({ email: 'guest@example.com', name: 'Guest User' });
    setIsLoggedIn(true);
    setSessionId(`guest_${Date.now()}`);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setSessionId(null);
    setMessages([]);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    const messagesContainer = document.querySelector(".messages-container");
    if (messagesContainer) {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }, [messages, isTyping]);

    return (
    <AppContainer>
      <FloatingParticles />
      
      {!isLoggedIn ? (
        <Login onLogin={handleLogin} onGuestLogin={handleGuestLogin} />
      ) : (
        <>
          <Header user={user} onLogout={handleLogout} />
          
          <ChatContainer
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
        {messages.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            <WelcomeMessage>
              <h2>Welcome to SATURDAY 🤖</h2>
              <p>
                Your empathetic AI companion that understands emotions and
                provides meaningful conversations.
              </p>

              <FeaturesGrid>
                <FeatureCard
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <Brain size={40} color="#fff" />
                  <h3>Emotion AI</h3>
                  <p>Advanced emotion detection using NLP</p>
                </FeatureCard>

                <FeatureCard
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <Heart size={40} color="#fff" />
                  <h3>Empathetic</h3>
                  <p>Human-like responses with understanding</p>
                </FeatureCard>

                <FeatureCard
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <Sparkles size={40} color="#fff" />
                  <h3>Real-time</h3>
                  <p>Instant responses and smooth interactions</p>
                </FeatureCard>
              </FeaturesGrid>
            </WelcomeMessage>
          </motion.div>
        ) : (
          <MessagesContainer className="messages-container">
            <AnimatePresence>
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
              {isTyping && <TypingIndicator />}
            </AnimatePresence>
          </MessagesContainer>
        )}

        <InputContainer
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts with SATURDAY..."
            disabled={isLoading}
          />
          <SendButton
            onClick={sendMessage}
            disabled={!inputValue.trim() || isLoading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Send size={20} />
          </SendButton>
                    </InputContainer>
          </ChatContainer>
        </>
      )}
    </AppContainer>
  );
}

export default App;
