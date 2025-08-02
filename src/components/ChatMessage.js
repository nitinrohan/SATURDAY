import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { User, Bot } from "lucide-react";

const MessageContainer = styled(motion.div)`
  display: flex;
  margin-bottom: 20px;
  gap: 12px;
  align-items: flex-start;

  ${(props) =>
    props.sender === "user" &&
    `
    flex-direction: row-reverse;
    gap: 12px;
  `}
`;

const Avatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

  ${(props) =>
    props.sender === "user"
      ? `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  `
      : `
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    color: white;
  `}
`;

const MessageBubble = styled(motion.div)`
  max-width: 70%;
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  word-wrap: break-word;

  ${(props) =>
    props.sender === "user"
      ? `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 4px;
    margin-left: auto;
  `
      : `
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-bottom-left-radius: 4px;
  `}

  .message-text {
    font-size: 15px;
    line-height: 1.4;
    margin-bottom: 4px;
  }

  .message-emoji {
    font-size: 18px;
    margin-left: 8px;
  }

  .message-time {
    font-size: 11px;
    opacity: 0.7;
    margin-top: 4px;
  }

  .emotion-indicator {
    position: absolute;
    top: -8px;
    left: 16px;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
`;

const ChatMessage = ({ message }) => {
  const isUser = message.sender === "user";

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <MessageContainer
      sender={message.sender}
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{
        duration: 0.3,
        ease: "easeOut",
        delay: isUser ? 0 : 0.1,
      }}
    >
      <Avatar sender={message.sender}>
        {isUser ? <User size={20} /> : <Bot size={20} />}
      </Avatar>

      <MessageBubble
        sender={message.sender}
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 25,
          delay: 0.1,
        }}
      >
        {!isUser && message.emotion && (
          <div className="emotion-indicator">{message.emotion}</div>
        )}

        <div className="message-text">
          {message.text}
          {!isUser && message.emoji && (
            <span className="message-emoji">{message.emoji}</span>
          )}
        </div>

        <div className="message-time">{formatTime(message.timestamp)}</div>
      </MessageBubble>
    </MessageContainer>
  );
};

export default ChatMessage;
