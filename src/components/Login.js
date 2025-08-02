import React, { useState } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, EyeOff, Mail, Lock, Bot, Sparkles, ArrowRight, User } from 'lucide-react';

const LoginContainer = styled(motion.div)`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
  
  @media (max-width: 768px) {
    padding: 16px;
  }
  
  @media (max-width: 480px) {
    padding: 12px;
  }
`;

const BackgroundParticles = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
`;

const Particle = styled(motion.div)`
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  pointer-events: none;
`;

const LoginCard = styled(motion.div)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 48px;
  width: 100%;
  max-width: 420px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
  
  @media (max-width: 768px) {
    padding: 32px 24px;
    margin: 20px;
    max-width: calc(100% - 40px);
  }
  
  @media (max-width: 480px) {
    padding: 24px 16px;
    margin: 16px;
    max-width: calc(100% - 32px);
  }
`;

const Logo = styled.div`
  text-align: center;
  margin-bottom: 32px;
  
  .logo-icon {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 50%;
    width: 64px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  }
  
  h1 {
    color: white;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 8px;
    background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1rem;
    font-weight: 400;
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const InputGroup = styled.div`
  position: relative;
  
  .input-icon {
    position: absolute;
    left: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.6);
    z-index: 2;
  }
  
  .password-toggle {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    z-index: 2;
    transition: color 0.3s ease;
    
    &:hover {
      color: rgba(255, 255, 255, 0.8);
    }
  }
`;

const Input = styled.input`
  width: 100%;
  padding: 16px 16px 16px 48px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  color: white;
  font-size: 16px;
  font-weight: 400;
  outline: none;
  transition: all 0.3s ease;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
  
  &:focus {
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
  }
  
  &:hover {
    border-color: rgba(255, 255, 255, 0.3);
  }
`;

const LoginButton = styled(motion.button)`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  padding: 16px;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const Divider = styled.div`
  display: flex;
  align-items: center;
  margin: 24px 0;
  
  .line {
    flex: 1;
    height: 1px;
    background: rgba(255, 255, 255, 0.2);
  }
  
  .text {
    color: rgba(255, 255, 255, 0.6);
    padding: 0 16px;
    font-size: 14px;
  }
`;

const GuestButton = styled(motion.button)`
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 16px;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
  }
`;

const ErrorMessage = styled(motion.div)`
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  padding: 12px;
  color: #fca5a5;
  font-size: 14px;
  text-align: center;
`;

const Features = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 24px;
`;

const Feature = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  
  .feature-icon {
    color: #4ade80;
  }
`;

const Login = ({ onLogin, onGuestLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      if (isRegistering) {
        // Handle registration
        if (!email || !password || !name) {
          setError('Please fill in all fields');
          setIsLoading(false);
          return;
        }
        
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ email, password, name }),
        });
        
        const result = await response.json();
        
        if (result.success) {
          // Auto-login after successful registration
          onLogin({ email, password });
        } else {
          setError(result.message);
        }
      } else {
        // Handle login
        if (!email || !password) {
          setError('Please fill in all fields');
          setIsLoading(false);
          return;
        }
        
        onLogin({ email, password });
      }
    } catch (error) {
      console.error('Auth error:', error);
      setError('An error occurred. Please try again.');
    }
    
    setIsLoading(false);
  };

  const handleGuestLogin = () => {
    onGuestLogin();
  };

  const particles = Array.from({ length: 15 }, (_, i) => ({
    id: i,
    size: Math.random() * 6 + 2,
    x: Math.random() * 100,
    y: Math.random() * 100,
    duration: Math.random() * 20 + 15,
    delay: Math.random() * 5
  }));

  return (
    <LoginContainer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <BackgroundParticles>
        {particles.map((particle) => (
          <Particle
            key={particle.id}
            style={{
              width: particle.size,
              height: particle.size,
              left: `${particle.x}%`,
              top: `${particle.y}%`,
            }}
            animate={{
              y: [0, -100, 0],
              x: [0, Math.random() * 50 - 25, 0],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: particle.duration,
              repeat: Infinity,
              delay: particle.delay,
              ease: "easeInOut",
            }}
          />
        ))}
      </BackgroundParticles>

      <LoginCard
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        <Logo>
          <div className="logo-icon">
            <Bot size={32} color="white" />
          </div>
          <h1>SATURDAY</h1>
          <p>Your empathetic AI companion</p>
        </Logo>

        <Form onSubmit={handleSubmit}>
          {isRegistering && (
            <InputGroup>
              <User size={20} className="input-icon" />
              <Input
                type="text"
                placeholder="Full name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required={isRegistering}
              />
            </InputGroup>
          )}
          
          <InputGroup>
            <Mail size={20} className="input-icon" />
            <Input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </InputGroup>

          <InputGroup>
            <Lock size={20} className="input-icon" />
            <Input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <div
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </div>
          </InputGroup>

          <AnimatePresence>
            {error && (
              <ErrorMessage
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                {error}
              </ErrorMessage>
            )}
          </AnimatePresence>

                           <LoginButton
                   type="submit"
                   disabled={isLoading}
                   whileHover={{ scale: 1.02 }}
                   whileTap={{ scale: 0.98 }}
                 >
                   {isLoading ? (
                     <>
                       <motion.div
                         animate={{ rotate: 360 }}
                         transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                       >
                         <Sparkles size={20} />
                       </motion.div>
                       {isRegistering ? 'Creating account...' : 'Signing in...'}
                     </>
                   ) : (
                     <>
                       {isRegistering ? 'Create Account' : 'Sign In'}
                       <ArrowRight size={20} />
                     </>
                   )}
                 </LoginButton>

          <Divider>
            <div className="line" />
            <span className="text">or</span>
            <div className="line" />
          </Divider>

                           <GuestButton
                   type="button"
                   onClick={handleGuestLogin}
                   whileHover={{ scale: 1.02 }}
                   whileTap={{ scale: 0.98 }}
                 >
                   <Bot size={20} />
                   Continue as Guest
                 </GuestButton>
                 
                 <div style={{ textAlign: 'center', marginTop: '16px' }}>
                   <button
                     type="button"
                     onClick={() => {
                       setIsRegistering(!isRegistering);
                       setError('');
                       setName('');
                     }}
                     style={{
                       background: 'none',
                       border: 'none',
                       color: 'rgba(255, 255, 255, 0.8)',
                       cursor: 'pointer',
                       fontSize: '14px',
                       textDecoration: 'underline',
                       padding: '8px',
                     }}
                   >
                     {isRegistering ? 'Already have an account? Sign In' : "Don't have an account? Register"}
                   </button>
                 </div>
        </Form>

        <Features>
          <Feature>
            <Sparkles size={16} className="feature-icon" />
            Emotion AI
          </Feature>
          <Feature>
            <Sparkles size={16} className="feature-icon" />
            Real-time Chat
          </Feature>
          <Feature>
            <Sparkles size={16} className="feature-icon" />
            Privacy First
          </Feature>
          <Feature>
            <Sparkles size={16} className="feature-icon" />
            Always Available
          </Feature>
        </Features>
      </LoginCard>
    </LoginContainer>
  );
};

export default Login; 