import React, { useState, useRef, useEffect } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! How can I help you today?' },
  ]); // Initialize with a welcome message
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const chatHistory = messages.map(msg => ({ role: msg.role, content: msg.content }));

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: input, chat_history: chatHistory }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, there was an error processing your request.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chatContainer">
      <div className="messagesBox">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${
              message.role === 'user' ? 'userMessage' : 'aiMessage'
            }`}
          >
            <div>{message.content}</div>
            {message.sources && message.sources.length > 0 && (
              <div>
                <h4>Sources:</h4>
                {message.sources.map((source, idx) => (
                  <div key={idx}>
                    <p>{source.metadata?.source || 'Unknown Source'} (Chunk: {source.metadata?.chunk || 'N/A'})</p>
                    <p>{source.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="message aiMessage">
            <div>Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="inputBox">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about the financial statement..."
          disabled={isLoading}
          className="chatInput"
        />
        <button type="submit" disabled={isLoading || !input.trim()} className="sendButton">
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface; 