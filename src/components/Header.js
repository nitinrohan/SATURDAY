import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { Bot, Sparkles } from "lucide-react";

const HeaderContainer = styled(motion.header)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: 20px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  
  @media (max-width: 768px) {
    padding: 16px 0;
  }
  
  @media (max-width: 480px) {
    padding: 12px 0;
  }
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  @media (max-width: 768px) {
    padding: 0 16px;
  }
  
  @media (max-width: 480px) {
    padding: 0 12px;
  }
`;

const Logo = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 12px;
  color: white;

  h1 {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    
    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
    
    @media (max-width: 480px) {
      font-size: 1.3rem;
    }
  }

  .logo-icon {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }
`;

const StatusIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 0.9rem;
  font-weight: 500;

  .status-dot {
    width: 8px;
    height: 8px;
    background: #4ade80;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%,
    100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
`;

const Header = ({ user, onLogout }) => {
  return (
    <HeaderContainer
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      <HeaderContent>
        <Logo
          whileHover={{ scale: 1.05 }}
          transition={{ type: "spring", stiffness: 300 }}
        >
          <div className="logo-icon">
            <Bot size={24} color="white" />
          </div>
          <h1>SATURDAY</h1>
        </Logo>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          <StatusIndicator
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <div className="status-dot" />
            <span>AI Online</span>
            <Sparkles size={16} />
          </StatusIndicator>
          
          {user && (
            <motion.div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                color: 'white',
                fontSize: '0.9rem',
                fontWeight: '500'
              }}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
            >
              <span>Welcome, {user.name}</span>
              <motion.button
                onClick={onLogout}
                style={{
                  background: 'rgba(255, 255, 255, 0.1)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  borderRadius: '8px',
                  padding: '8px 12px',
                  color: 'white',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '0.8rem'
                }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <LogOut size={14} />
                Logout
              </motion.button>
            </motion.div>
          )}
        </div>
      </HeaderContent>
    </HeaderContainer>
  );
};

export default Header;
