import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { Bot } from "lucide-react";

const TypingContainer = styled(motion.div)`
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 20px;
`;

const Avatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
`;

const TypingBubble = styled(motion.div)`
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 18px;
  border-bottom-left-radius: 4px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 4px;
  color: white;
  font-size: 14px;
`;

const Dot = styled(motion.div)`
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
`;

const TypingIndicator = () => {
  return (
    <TypingContainer
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Avatar>
        <Bot size={20} />
      </Avatar>

      <TypingBubble
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{
          type: "spring",
          stiffness: 300,
          damping: 25,
        }}
      >
        <span>SATURDAY is typing</span>
        <Dot
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{
            duration: 1.4,
            repeat: Infinity,
            delay: 0,
          }}
        />
        <Dot
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{
            duration: 1.4,
            repeat: Infinity,
            delay: 0.2,
          }}
        />
        <Dot
          animate={{ opacity: [0.4, 1, 0.4] }}
          transition={{
            duration: 1.4,
            repeat: Infinity,
            delay: 0.4,
          }}
        />
      </TypingBubble>
    </TypingContainer>
  );
};

export default TypingIndicator;
