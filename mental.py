
import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, LogOut, User, Moon, Sun, Volume2, VolumeX } from 'lucide-react';

const ChillApp = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [authMode, setAuthMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [isSoundEnabled, setIsSoundEnabled] = useState(true);
  const [isTyping, setIsTyping] = useState(false);
  
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    const savedAuth = localStorage.getItem('chillAuth');
    if (savedAuth) {
      const userData = JSON.parse(savedAuth);
      setIsAuthenticated(true);
      setCurrentUser(userData);
      loadUserMessages(userData.email);
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadUserMessages = (userEmail) => {
    const saved = localStorage.getItem(`chillMessages_${userEmail}`);
    if (saved) {
      setMessages(JSON.parse(saved));
    } else {
      setMessages([{
        type: 'ai',
        text: `Welcome to Chill. I'm here to listen and support you. How are you feeling today?`,
        timestamp: new Date().toISOString()
      }]);
    }
  };

  const saveMessages = (msgs, userEmail) => {
    localStorage.setItem(`chillMessages_${userEmail}`, JSON.stringify(msgs));
  };

  const handleAuth = (e) => {
    e.preventDefault();
    
    if (authMode === 'signup') {
      if (!name || !email || !password) {
        alert('Please fill in all fields');
        return;
      }
      const userData = { name, email };
      localStorage.setItem('chillAuth', JSON.stringify(userData));
      localStorage.setItem(`chillPass_${email}`, password);
      setCurrentUser(userData);
      setIsAuthenticated(true);
      loadUserMessages(email);
    } else {
      const savedPass = localStorage.getItem(`chillPass_${email}`);
      if (savedPass === password) {
        const userData = { name: email.split('@')[0], email };
        localStorage.setItem('chillAuth', JSON.stringify(userData));
        setCurrentUser(userData);
        setIsAuthenticated(true);
        loadUserMessages(email);
      } else {
        alert('Invalid credentials');
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('chillAuth');
    setIsAuthenticated(false);
    setCurrentUser(null);
    setMessages([]);
  };

  const getAIResponse = async (userMessage) => {
    const lowerMsg = userMessage.toLowerCase();
    
    // Therapeutic responses based on keywords
    if (lowerMsg.includes('stress') || lowerMsg.includes('anxious') || lowerMsg.includes('anxiety')) {
      return "I hear that you're feeling stressed. That's completely valid. Let's try a quick breathing exercise: Breathe in for 4 counts, hold for 4, then exhale for 6. Would you like to talk about what's causing this stress?";
    } else if (lowerMsg.includes('sad') || lowerMsg.includes('depressed') || lowerMsg.includes('down')) {
      return "I'm sorry you're feeling this way. Your feelings are important and valid. Remember that it's okay to not be okay sometimes. What's been weighing on your mind?";
    } else if (lowerMsg.includes('sleep') || lowerMsg.includes('insomnia') || lowerMsg.includes('tired')) {
      return "Sleep difficulties can be really challenging. Have you tried creating a bedtime routine? Avoiding screens 30 minutes before bed and practicing relaxation techniques can help. What's your sleep environment like?";
    } else if (lowerMsg.includes('work') || lowerMsg.includes('job')) {
      return "Work-related stress is very common. It's important to set boundaries and take breaks. Have you been able to take time for yourself outside of work?";
    } else if (lowerMsg.includes('thank') || lowerMsg.includes('better') || lowerMsg.includes('good')) {
      return "I'm so glad to hear that! Remember, I'm always here when you need support. Taking care of your mental health is a journey, and you're doing great.";
    } else if (lowerMsg.includes('help') || lowerMsg.includes('advice')) {
      return "I'm here to listen and support you. While I can provide coping strategies, please remember that for serious concerns, reaching out to a mental health professional is important. What would you like to talk about?";
    } else {
      return "Thank you for sharing that with me. Your feelings are valid. Tell me more about what you're experiencing. I'm here to listen without judgment.";
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = {
      type: 'user',
      text: input,
      timestamp: new Date().toISOString()
    };

    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInput('');
    setIsTyping(true);

    // Simulate AI thinking time
    setTimeout(async () => {
      const aiResponse = await getAIResponse(input);
      const aiMsg = {
        type: 'ai',
        text: aiResponse,
        timestamp: new Date().toISOString()
      };
      const finalMessages = [...updatedMessages, aiMsg];
      setMessages(finalMessages);
      saveMessages(finalMessages, currentUser.email);
      setIsTyping(false);
    }, 1000 + Math.random() * 1000);
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      audioChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        audioChunksRef.current.push(e.data);
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        
        const voiceMsg = {
          type: 'user',
          text: '[Voice Note]',
          audio: audioUrl,
          timestamp: new Date().toISOString()
        };
        
        const updatedMessages = [...messages, voiceMsg];
        setMessages(updatedMessages);
        saveMessages(updatedMessages, currentUser.email);
        
        stream.getTracks().forEach(track => track.stop());
        
        // AI responds to voice note
        setTimeout(() => {
          const aiMsg = {
            type: 'ai',
            text: "Thank you for sharing that voice note with me. I'm here to listen. Would you like to tell me more about how you're feeling?",
            timestamp: new Date().toISOString()
          };
          const finalMessages = [...updatedMessages, aiMsg];
          setMessages(finalMessages);
          saveMessages(finalMessages, currentUser.email);
        }, 1500);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (err) {
      alert('Microphone access denied. Please enable microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className={`min-h-screen flex items-center justify-center ${isDarkMode ? 'bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900' : 'bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100'}`}>
        <div className={`${isDarkMode ? 'bg-gray-800/50' : 'bg-white/80'} backdrop-blur-lg p-8 rounded-3xl shadow-2xl w-96 border ${isDarkMode ? 'border-purple-500/30' : 'border-purple-300'}`}>
          <div className="text-center mb-6">
            <h1 className={`text-4xl font-bold ${isDarkMode ? 'text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400' : 'text-purple-600'}`}>
              Chill
            </h1>
            <p className={`${isDarkMode ? 'text-gray-300' : 'text-gray-600'} mt-2`}>Your mental wellness companion</p>
          </div>

          <form onSubmit={handleAuth} className="space-y-4">
            {authMode === 'signup' && (
              <input
                type="text"
                placeholder="Full Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className={`w-full px-4 py-3 rounded-xl ${isDarkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-gray-100 text-gray-900 border-gray-300'} border focus:outline-none focus:ring-2 focus:ring-purple-500`}
              />
            )}
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={`w-full px-4 py-3 rounded-xl ${isDarkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-gray-100 text-gray-900 border-gray-300'} border focus:outline-none focus:ring-2 focus:ring-purple-500`}
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={`w-full px-4 py-3 rounded-xl ${isDarkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-gray-100 text-gray-900 border-gray-300'} border focus:outline-none focus:ring-2 focus:ring-purple-500`}
            />
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white py-3 rounded-xl font-semibold hover:from-purple-600 hover:to-pink-600 transition-all duration-300 shadow-lg"
            >
              {authMode === 'signup' ? 'Sign Up' : 'Log In'}
            </button>
          </form>

          <div className="mt-4 text-center">
            <button
              onClick={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')}
              className={`${isDarkMode ? 'text-purple-400' : 'text-purple-600'} hover:underline`}
            >
              {authMode === 'login' ? 'Need an account? Sign up' : 'Have an account? Log in'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${isDarkMode ? 'bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900' : 'bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50'}`}>
      {/* Header */}
      <div className={`${isDarkMode ? 'bg-gray-800/50' : 'bg-white/80'} backdrop-blur-lg border-b ${isDarkMode ? 'border-purple-500/30' : 'border-purple-200'} px-6 py-4 flex items-center justify-between shadow-lg`}>
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
            <User size={20} className="text-white" />
          </div>
          <div>
            <h2 className={`font-semibold ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>{currentUser?.name}</h2>
            <p className={`text-xs ${isDarkMode ? 'text-gray-400' : 'text-gray-600'}`}>Online</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setIsSoundEnabled(!isSoundEnabled)}
            className={`p-2 rounded-full ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-200'} transition-colors`}
          >
            {isSoundEnabled ? <Volume2 size={20} className={isDarkMode ? 'text-gray-300' : 'text-gray-600'} /> : <VolumeX size={20} className={isDarkMode ? 'text-gray-300' : 'text-gray-600'} />}
          </button>
          <button
            onClick={() => setIsDarkMode(!isDarkMode)}
            className={`p-2 rounded-full ${isDarkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-200'} transition-colors`}
          >
            {isDarkMode ? <Sun size={20} className="text-yellow-400" /> : <Moon size={20} className="text-gray-600" />}
          </button>
          <button
            onClick={handleLogout}
            className="flex items-center space-x-2 px-4 py-2 bg-red-500/20 hover:bg-red-500/30 rounded-full transition-colors"
          >
            <LogOut size={18} className="text-red-400" />
            <span className="text-red-400 font-medium">Logout</span>
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="h-[calc(100vh-180px)] overflow-y-auto px-6 py-6 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] rounded-2xl px-5 py-3 ${
              msg.type === 'user'
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
                : isDarkMode ? 'bg-gray-800/70 text-gray-200' : 'bg-white text-gray-900'
            } shadow-lg`}>
              {msg.audio ? (
                <div>
                  <p className="mb-2">{msg.text}</p>
                  <audio controls className="w-full">
                    <source src={msg.audio} type="audio/wav" />
                  </audio>
                </div>
              ) : (
                <p className="leading-relaxed">{msg.text}</p>
              )}
              <p className={`text-xs mt-2 ${msg.type === 'user' ? 'text-purple-100' : isDarkMode ? 'text-gray-500' : 'text-gray-500'}`}>
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className={`rounded-2xl px-5 py-3 ${isDarkMode ? 'bg-gray-800/70' : 'bg-white'} shadow-lg`}>
              <div className="flex space-x-2">
                <div className={`w-2 h-2 ${isDarkMode ? 'bg-gray-500' : 'bg-gray-400'} rounded-full animate-bounce`} style={{ animationDelay: '0ms' }}></div>
                <div className={`w-2 h-2 ${isDarkMode ? 'bg-gray-500' : 'bg-gray-400'} rounded-full animate-bounce`} style={{ animationDelay: '150ms' }}></div>
                <div className={`w-2 h-2 ${isDarkMode ? 'bg-gray-500' : 'bg-gray-400'} rounded-full animate-bounce`} style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className={`${isDarkMode ? 'bg-gray-800/50' : 'bg-white/80'} backdrop-blur-lg border-t ${isDarkMode ? 'border-purple-500/30' : 'border-purple-200'} px-6 py-4`}>
        <div className="flex items-center space-x-3">
          <button
            onMouseDown={startRecording}
            onMouseUp={stopRecording}
            onTouchStart={startRecording}
            onTouchEnd={stopRecording}
            className={`p-3 rounded-full ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-gradient-to-r from-purple-500 to-pink-500'} hover:opacity-90 transition-all duration-300 shadow-lg`}
          >
            <Mic size={24} className="text-white" />
          </button>
          
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Share how you're feeling..."
            className={`flex-1 px-5 py-3 rounded-full ${isDarkMode ? 'bg-gray-700 text-white border-gray-600' : 'bg-gray-100 text-gray-900 border-gray-300'} border focus:outline-none focus:ring-2 focus:ring-purple-500`}
          />
          
          <button
            onClick={handleSendMessage}
            className="p-3 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 hover:opacity-90 transition-all duration-300 shadow-lg"
          >
            <Send size={24} className="text-white" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChillApp;