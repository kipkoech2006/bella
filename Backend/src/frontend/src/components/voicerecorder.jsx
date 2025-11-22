javascript
import { useState, useRef } from 'react';

export default function VoiceRecorder({ onTranscript }) {
  const [isRecording, setIsRecording] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef(null);

  const startRecording = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Speech recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognitionRef.current.start();
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsRecording(false);
      if (transcript.trim()) {
        onTranscript(transcript.trim());
        setTranscript('');
      }
    }
  };

  return (
    
      
        {isRecording ? '⏹️ Stop Recording' : '🎤 Voice Note'}
      
      {isRecording && transcript && (
        {transcript}
      )}
    
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px',
  },
  button: {
    padding: '10px 16px',
    background: '#667eea',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    fontSize: '14px',
    cursor: 'pointer',
    transition: 'all 0.3s',
  },
  buttonRecording: {
    background: '#e53e3e',
    animation: 'pulse 1.5s infinite',
  },
  transcript: {
    padding: '8px',
    background: '#f7fafc',
    borderRadius: '6px',
    fontSize: '14px',
    color: '#666',
    fontStyle: 'italic',
  },
};