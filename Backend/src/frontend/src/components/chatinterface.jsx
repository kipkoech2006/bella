javascript
import { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../services/api';
import VoiceRecorder from './VoiceRecorder';

export default function ChatInterface({ user, onLogout }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadHistory = async () => {
    try {
      const response = await chatAPI.getHistory();
      setMessages(response.data);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (messageText, messageType = 'text') => {
    if (!messageText.trim()) return;

    const userMessage = { role: 'user', content: messageText, message_type: messageType };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatAPI.sendMessage(messageText, messageType);
      const aiMessage = { role: 'assistant', content: response.data.message, message_type: 'text' };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.', 
        message_type: 'text' 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage(input, 'text');
  };

  const handleVoiceTranscript = (transcript) => {
    sendMessage(transcript, 'voice');
  };

  const handleClearHistory = async () => {
    if (window.confirm('Are you sure you want to clear your conversation history?')) {
      try {
        await chatAPI.clearHistory();
        setMessages([]);
      } catch (error) {
        console.error('Failed to clear history:', error);
        alert('Failed to clear history. Please try again.');
      }
    }
  };

  return (
    
      
        
          Chill 🌿
          Your AI mental health companion
        
        
          {user.name}
          
            Clear Chat
          
          
            Logout
          
        
      

      
        {messages.length === 0 && (
          
            Welcome to Chill
            
              I'm here to listen and support you. Share what's on your mind, either by typing or using voice notes.
            
          
        )}
        
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              ...styles.message,
              ...(msg.role === 'user' ? styles.userMessage : styles.aiMessage),
            }}
          >
            
              {msg.message_type === 'voice' && msg.role === 'user' && (
                🎤 Voice Note
              )}
              {msg.content}
            
          
        ))}
        
        {loading && (
          
            
            
            
          
        )}
        
        
      

      
        
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Share what's on your mind..."
            style={styles.input}
            disabled={loading}
          />
          
            Send
          
        
        
      
    
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    background: '#f7fafc',
  },
  header: {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '20px 30px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  title: {
    margin: 0,
    fontSize: '24px',
    fontWeight: 'bold',
  },
  subtitle: {
    margin: '4px 0 0 0',
    fontSize: '14px',
    opacity: 0.9,
  },
  headerActions: {
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
  },
  userName: {
    fontSize: '14px',
    fontWeight: '500',
  },
  clearButton: {
    padding: '8px 16px',
    background: 'rgba(255,255,255,0.2)',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
  },
  logoutButton: {
    padding: '8px 16px',
    background: 'white',
    color: '#667eea',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '600',
  },
  messagesContainer: {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  emptyState: {
    textAlign: 'center',
    marginTop: '60px',
    padding: '40px',
  },
  emptyTitle: {
    fontSize: '28px',
    color: '#333',
    marginBottom: '12px',
  },
  emptyText: {
    fontSize: '16px',
    color: '#666',
    maxWidth: '500px',
    margin: '0 auto',
    lineHeight: '1.6',
  },
  message: {
    maxWidth: '70%',
    padding: '12px 16px',
    borderRadius: '12px',
    wordWrap: 'break-word',
  },
  userMessage: {
    alignSelf: 'flex-end',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    borderBottomRightRadius: '4px',
  },
  aiMessage: {
    alignSelf: 'flex-start',
    background: 'white',
    color: '#333',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    borderBottomLeftRadius: '4px',
  },
  messageContent: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  voiceBadge: {
    fontSize: '12px',
    opacity: 0.8,
    fontStyle: 'italic',
  },
  messageText: {
    margin: 0,
    lineHeight: '1.5',
  },
  loadingContainer: {
    display: 'flex',
    gap: '6px',
    padding: '12px 16px',
    background: 'white',
    borderRadius: '12px',
    width: 'fit-content',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
  },
  loadingDot: {
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: '#667eea',
    animation: 'bounce 1.4s infinite ease-in-out both',
  },
  inputContainer: {
    background: 'white',
    padding: '20px',
    borderTop: '1px solid #e0e0e0',
    display: 'flex',
    flexDirection: 'column',
    gap: '12px',
  },
  form: {
    display: 'flex',
    gap: '12px',
  },
  input: {
    flex: 1,
    padding: '14px 16px',
    border: '2px solid #e0e0e0',
    borderRadius: '8px',
    fontSize: '16px',
    outline: 'none',
  },
  sendButton: {
    padding: '14px 32px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
  },
};