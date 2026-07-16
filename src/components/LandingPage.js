import React from "react";
import styled from "styled-components";
import { motion } from "framer-motion";
import { Heart, Brain, MessageCircle, ShieldCheck, Check } from "lucide-react";

/* ---------- layout ---------- */
const Page = styled.div`
  position: relative;
  z-index: 2;
  color: var(--text);
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px 80px;
`;

const Nav = styled.header`
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
  backdrop-filter: blur(10px);
`;

const Brand = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: "Space Grotesk", sans-serif;
  font-weight: 700;
  font-size: 20px;

  .orb {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, var(--cyan), var(--violet), var(--pink), var(--cyan));
    box-shadow: 0 0 18px rgba(139, 92, 246, 0.7);
    animation: spin 8s linear infinite;
  }
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;

const NavLinks = styled.nav`
  display: flex;
  align-items: center;
  gap: 28px;
  font-size: 15px;

  a {
    color: var(--muted);
    text-decoration: none;
    transition: color 0.2s;
    &:hover {
      color: var(--text);
    }
  }
  @media (max-width: 760px) {
    a:not(.cta) {
      display: none;
    }
  }
`;

const Btn = styled(motion.button)`
  font-family: "Inter", sans-serif;
  font-weight: 600;
  font-size: 15px;
  padding: 13px 26px;
  border-radius: 999px;
  border: 1px solid transparent;
  cursor: pointer;
  color: #fff;
  background: linear-gradient(120deg, var(--violet), var(--indigo) 60%, var(--cyan));
  box-shadow: 0 18px 40px -14px var(--violet);

  &.ghost {
    background: var(--glass);
    border-color: var(--glass-brd);
    color: var(--text);
    box-shadow: none;
    backdrop-filter: blur(8px);
  }
  &.full {
    width: 100%;
  }
`;

/* ---------- hero ---------- */
const Hero = styled.section`
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 48px;
  align-items: center;
  padding: 60px 0 40px;
  min-height: 72vh;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 32px 0;
  }
`;

const Eyebrow = styled.span`
  display: inline-block;
  font-size: 13px;
  color: var(--cyan);
  border: 1px solid rgba(34, 211, 238, 0.3);
  background: rgba(34, 211, 238, 0.06);
  padding: 6px 14px;
  border-radius: 999px;
  margin-bottom: 22px;
`;

const Title = styled.h1`
  font-family: "Space Grotesk", sans-serif;
  font-size: clamp(40px, 6.4vw, 68px);
  line-height: 1.03;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 0;

  .grad {
    background: linear-gradient(120deg, var(--cyan), var(--violet) 45%, var(--pink));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }
`;

const Sub = styled.p`
  color: var(--muted);
  font-size: 18px;
  line-height: 1.6;
  max-width: 54ch;
  margin: 22px 0 30px;
  @media (max-width: 900px) {
    margin-left: auto;
    margin-right: auto;
  }
`;

const Actions = styled.div`
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  @media (max-width: 900px) {
    justify-content: center;
  }
`;

const Note = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 28px;
  color: var(--muted);
  font-size: 14px;
  @media (max-width: 900px) {
    justify-content: center;
  }
  strong {
    color: var(--text);
  }
  .dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 12px var(--cyan);
  }
`;

const OrbCard = styled(motion.div)`
  position: relative;
  width: 100%;
  max-width: 340px;
  aspect-ratio: 1;
  margin: 0 auto;
  border-radius: 32px;
  border: 1px solid var(--glass-brd);
  background: radial-gradient(120% 120% at 30% 20%, rgba(139, 92, 246, 0.28), rgba(6, 6, 13, 0.2) 60%);
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  box-shadow: var(--shadow);

  .pulse {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #fff, var(--cyan) 30%, var(--violet) 70%);
    box-shadow: 0 0 60px rgba(139, 92, 246, 0.8);
    animation: breathe 4s ease-in-out infinite;
  }
  @keyframes breathe {
    0%, 100% { transform: scale(1); opacity: 0.9; }
    50% { transform: scale(1.12); opacity: 1; }
  }
  .caption { color: var(--muted); font-size: 14px; }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; }
  .chips span {
    font-size: 13px;
    padding: 5px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid var(--glass-brd);
  }
`;

/* ---------- shared section ---------- */
const Section = styled.section`
  padding: 70px 0;
`;
const Head = styled.div`
  text-align: center;
  max-width: 60ch;
  margin: 0 auto 46px;

  .kicker {
    font-size: 13px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--violet);
    font-weight: 600;
  }
  h2 {
    font-family: "Space Grotesk", sans-serif;
    font-size: clamp(28px, 4.4vw, 40px);
    margin-top: 12px;
    line-height: 1.12;
  }
`;

const Glass = styled(motion.div)`
  background: var(--glass);
  border: 1px solid var(--glass-brd);
  border-radius: 22px;
  backdrop-filter: blur(16px);
  box-shadow: var(--shadow);
`;

const Stats = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  text-align: center;
  padding: 10px 0 20px;
  @media (max-width: 760px) {
    grid-template-columns: 1fr;
  }
  b {
    display: block;
    font-family: "Space Grotesk", sans-serif;
    font-size: 34px;
  }
  span {
    color: var(--muted);
    font-size: 14.5px;
  }
`;

const Cards = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
`;
const Card = styled(Glass)`
  padding: 30px 26px;
  .ic {
    width: 52px;
    height: 52px;
    display: grid;
    place-items: center;
    border-radius: 16px;
    background: linear-gradient(140deg, rgba(139, 92, 246, 0.35), rgba(34, 211, 238, 0.2));
    margin-bottom: 18px;
  }
  h3 {
    font-family: "Space Grotesk", sans-serif;
    font-size: 21px;
    margin-bottom: 10px;
  }
  p {
    color: var(--muted);
    font-size: 15.5px;
    line-height: 1.55;
  }
`;

/* ---------- pricing ---------- */
const Pricing = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
  align-items: stretch;
  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
`;
const Price = styled(Glass)`
  padding: 30px 26px;
  display: flex;
  flex-direction: column;
  position: relative;

  &.featured {
    border-color: rgba(139, 92, 246, 0.6);
    background: linear-gradient(180deg, rgba(139, 92, 246, 0.14), var(--glass));
    @media (min-width: 901px) {
      transform: translateY(-10px);
    }
  }
  .badge {
    position: absolute;
    top: -14px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(120deg, var(--violet), var(--cyan));
    color: #fff;
    font-size: 12.5px;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 999px;
  }
  h3 { font-size: 19px; color: var(--muted); }
  .amount {
    font-family: "Space Grotesk", sans-serif;
    font-size: 54px;
    font-weight: 700;
    line-height: 1;
    margin: 12px 0 4px;
  }
  .amount .cur { font-size: 26px; vertical-align: super; color: var(--muted); }
  .amount .mo { font-size: 20px; color: var(--muted); }
  .per { color: var(--cyan); font-size: 14px; margin-bottom: 20px; }
  ul {
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 26px;
    flex: 1;
  }
  li {
    color: var(--muted);
    font-size: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  li svg { color: var(--cyan); flex-shrink: 0; }
`;

/* ---------- care ---------- */
const Care = styled(Glass)`
  display: flex;
  gap: 26px;
  padding: 40px;
  align-items: flex-start;
  @media (max-width: 760px) {
    flex-direction: column;
    text-align: center;
    align-items: center;
    padding: 28px;
  }
  .icon { flex-shrink: 0; color: var(--pink); }
  h2 { font-family: "Space Grotesk", sans-serif; font-size: 28px; margin-bottom: 14px; }
  p { color: var(--muted); font-size: 16px; margin-bottom: 12px; line-height: 1.6; }
  strong { color: var(--text); }
  .crisis {
    background: rgba(244, 114, 182, 0.1);
    border: 1px solid rgba(244, 114, 182, 0.3);
    border-radius: 14px;
    padding: 14px 18px;
    color: var(--text);
    font-size: 15px;
  }
`;

const Footer = styled.footer`
  margin-top: 70px;
  padding: 40px 0 16px;
  border-top: 1px solid var(--glass-brd);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: "Space Grotesk", sans-serif;
    font-weight: 700;
    font-size: 18px;
    .orb {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: conic-gradient(from 0deg, var(--cyan), var(--violet), var(--pink), var(--cyan));
      box-shadow: 0 0 14px rgba(139, 92, 246, 0.6);
    }
  }
  .tag {
    color: var(--muted);
    font-size: 14px;
    max-width: 48ch;
    line-height: 1.6;
  }
  .maker {
    margin-top: 6px;
    font-size: 13.5px;
    color: var(--text);
    letter-spacing: 0.04em;
  }
  .maker b {
    background: linear-gradient(120deg, var(--cyan), var(--violet) 55%, var(--pink));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
  }
  .fine {
    color: var(--muted);
    opacity: 0.7;
    font-size: 12.5px;
    margin-top: 4px;
  }
`;

const rise = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6 } },
};

const LandingPage = ({ onStart }) => {
  return (
    <Page>
      <Nav>
        <Brand>
          <span className="orb" />
          SATURDAY
        </Brand>
        <NavLinks>
          <a href="#how">How it works</a>
          <a href="#pricing">Pricing</a>
          <a href="#care">Your safety</a>
          <Btn className="cta" onClick={onStart} whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }}>
            Start talking
          </Btn>
        </NavLinks>
      </Nav>

      {/* HERO */}
      <Hero>
        <motion.div initial="hidden" animate="show" variants={rise}>
          <Eyebrow>Emotion-aware companion · available 24/7</Eyebrow>
          <Title>
            Therapy shouldn't be
            <br />
            a <span className="grad">luxury</span>.
          </Title>
          <Sub>
            Talking to someone costs too much for too many people. SATURDAY is a gentle,
            emotion-aware companion you can open up to - for the price of a coffee, not a co-pay.
            It listens, understands how you feel, and helps you make sense of it.
          </Sub>
          <Actions>
            <Btn onClick={onStart} whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }}>
              Start a conversation
            </Btn>
            <Btn as="a" href="#how" className="ghost" style={{ display: "inline-flex", alignItems: "center", textDecoration: "none" }}>
              See how it works
            </Btn>
          </Actions>
          <Note>
            <span className="dot" />
            A supportive first step - <strong>&nbsp;not&nbsp;</strong> a substitute for a licensed professional.
          </Note>
        </motion.div>

        <OrbCard
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          aria-hidden="true"
        >
          <div className="pulse" />
          <p className="caption">reading how you feel…</p>
          <div className="chips">
            <span>💙 calmer</span>
            <span>🤔 heard</span>
            <span>🌟 lighter</span>
          </div>
        </OrbCard>
      </Hero>

      {/* STATS */}
      <Stats>
        <div><b>1 in 5</b><span>adults live with a mental-health condition</span></div>
        <div><b>~60%</b><span>never get care - cost is the #1 barrier</span></div>
        <div><b>24/7</b><span>SATURDAY is here whenever it hits hardest</span></div>
      </Stats>

      {/* HOW */}
      <Section id="how">
        <Head>
          <span className="kicker">How it works</span>
          <h2>Three quiet steps to feeling a little lighter.</h2>
        </Head>
        <Cards>
          <Card initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }} variants={rise}>
            <div className="ic"><MessageCircle color="#fff" /></div>
            <h3>You talk, freely</h3>
            <p>Type whatever's on your mind - no forms, no judgement, no waiting room. Say as little or as much as you want.</p>
          </Card>
          <Card initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }} variants={rise}>
            <div className="ic"><Brain color="#fff" /></div>
            <h3>It understands</h3>
            <p>A fine-tuned model reads the emotion behind your words - sadness, fear, anger, joy - so replies actually meet you where you are.</p>
          </Card>
          <Card initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }} variants={rise}>
            <div className="ic"><Heart color="#fff" /></div>
            <h3>You feel heard</h3>
            <p>SATURDAY responds with empathy and gentle questions to help you untangle the knot - and points you onward when you need more.</p>
          </Card>
        </Cards>
      </Section>

      {/* PRICING */}
      <Section id="pricing">
        <Head>
          <span className="kicker">Pricing</span>
          <h2>Priced so cost is never the reason you don't reach out.</h2>
        </Head>
        <Pricing>
          <Price initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} variants={rise}>
            <h3>Just talk</h3>
            <div className="amount"><span className="cur">$</span>0</div>
            <p className="per">free, always</p>
            <ul>
              <li><Check size={18} />Unlimited conversations</li>
              <li><Check size={18} />Real-time emotion detection</li>
              <li><Check size={18} />No sign-up to get started</li>
            </ul>
            <Btn className="ghost full" onClick={onStart} whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }}>Start now</Btn>
          </Price>

          <Price className="featured" initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} variants={rise}>
            <span className="badge">Most helpful</span>
            <h3>Companion</h3>
            <div className="amount"><span className="cur">$</span>2.99<span className="mo">/mo</span></div>
            <p className="per">the price of a coffee</p>
            <ul>
              <li><Check size={18} />Everything in Just talk</li>
              <li><Check size={18} />Conversation history &amp; check-ins</li>
              <li><Check size={18} />Mood trends over time</li>
              <li><Check size={18} />Priority responses</li>
            </ul>
            <Btn className="full" onClick={onStart} whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }}>Try the companion</Btn>
          </Price>

          <Price initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.2 }} variants={rise}>
            <h3>Community</h3>
            <div className="amount"><span className="cur">$</span>0</div>
            <p className="per">sponsored seats</p>
            <ul>
              <li><Check size={18} />Full Companion access</li>
              <li><Check size={18} />For anyone who genuinely can't pay</li>
              <li><Check size={18} />Funded by paying members</li>
            </ul>
            <Btn className="ghost full" onClick={onStart} whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }}>Request a seat</Btn>
          </Price>
        </Pricing>
      </Section>

      {/* CARE */}
      <Section id="care">
        <Care initial="hidden" whileInView="show" viewport={{ once: true, amount: 0.3 }} variants={rise}>
          <ShieldCheck size={54} className="icon" />
          <div>
            <h2>We're a first step, not the whole journey.</h2>
            <p>
              SATURDAY can help you feel heard and take some weight off your shoulders - but it is{" "}
              <strong>not a doctor, therapist, or emergency service</strong>, and it can't diagnose or
              treat conditions. If you're in crisis or thinking about harming yourself, please reach out
              to a trained human right now.
            </p>
            <p className="crisis">
              🇺🇸 Call or text <strong>988</strong> (Suicide &amp; Crisis Lifeline) · 🇬🇧 <strong>116 123</strong>{" "}
              (Samaritans) · or your local emergency number. You deserve real support.
            </p>
          </div>
        </Care>
      </Section>

      <div style={{ textAlign: "center", paddingTop: 20 }}>
        <Btn onClick={onStart} whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }}>
          Talk to SATURDAY now
        </Btn>
      </div>

      <Footer>
        <div className="brand">
          <span className="orb" />
          SATURDAY
        </div>
        <p className="tag">
          Sentiment-Aware Textual Understanding and Response Dialogue Assistant - built to make
          a caring first conversation something everyone can afford.
        </p>
        <p className="maker">
          Designed &amp; built by <b>Nitin Sampath Rohan Bheemavarapu</b>
        </p>
        <p className="fine">
          © {new Date().getFullYear()} SATURDAY · A supportive companion, not medical advice.
        </p>
      </Footer>
    </Page>
  );
};

export default LandingPage;
