'use client';

import { useEffect, useMemo, useRef, useState } from 'react';

export function VoiceReader({ text, label = 'Read aloud' }: { text: string; label?: string }) {
  const [status, setStatus] = useState<'idle' | 'speaking' | 'paused'>('idle');
  const [supported, setSupported] = useState(false);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  const normalizedText = useMemo(() => {
    return text
      .replace(/<[^>]+>/g, ' ')
      .replace(/[#>*_`~]/g, ' ')
      .replace(/\{\s*\[/g, ' ')
      .replace(/\]\s*\}/g, ' ')
      .replace(/\{\s*question:/gi, ' Question: ')
      .replace(/\{\s*options:/gi, ' Options: ')
      .replace(/\s+/g, ' ')
      .trim();
  }, [text]);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window) {
      setSupported(true);
    }

    return () => {
      if (typeof window !== 'undefined') {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const stopReading = () => {
    if (typeof window === 'undefined') return;
    window.speechSynthesis.cancel();
    utteranceRef.current = null;
    setStatus('idle');
  };

  const startReading = () => {
    if (typeof window === 'undefined' || !supported || !normalizedText) return;

    const synth = window.speechSynthesis;
    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(normalizedText);
    utterance.lang = 'en-US';
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.onstart = () => setStatus('speaking');
    utterance.onpause = () => setStatus('paused');
    utterance.onresume = () => setStatus('speaking');
    utterance.onend = () => setStatus('idle');
    utterance.onerror = () => setStatus('idle');

    utteranceRef.current = utterance;
    synth.speak(utterance);
  };

  const handleToggle = () => {
    if (typeof window === 'undefined') return;

    if (status === 'speaking') {
      window.speechSynthesis.pause();
      setStatus('paused');
      return;
    }

    if (status === 'paused') {
      window.speechSynthesis.resume();
      setStatus('speaking');
      return;
    }

    startReading();
  };

  if (!supported || !normalizedText) {
    return null;
  }

  return (
    <div className="voice-reader" aria-live="polite">
      <button type="button" className="voice-reader-button" onClick={handleToggle}>
        {status === 'speaking' ? 'Pause voice' : status === 'paused' ? 'Resume voice' : label}
      </button>
      {(status === 'speaking' || status === 'paused') && (
        <button type="button" className="voice-reader-button secondary" onClick={stopReading}>
          Stop
        </button>
      )}
    </div>
  );
}
