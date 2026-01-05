import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import './TutorPanel.css';

import { ChatMessage } from '../services/api';

interface ContextExplanation {
    summary: string;
    grammar_notes: string;
    cultural_notes: string;
}

interface TutorPanelProps {
    explanation: ContextExplanation | null;
    originalText: string | null;
    loading: boolean;
    error: string | null;
    onClose: () => void;

    // Chat Props
    chatMessages: ChatMessage[];
    onSendMessage: (message: string) => void;
    isChatLoading: boolean;
}

const TutorPanel: React.FC<TutorPanelProps> = ({
    explanation,
    originalText,
    loading,
    error,
    onClose,
    chatMessages,
    onSendMessage,
    isChatLoading
}) => {
    const [input, setInput] = React.useState("");
    const messagesEndRef = React.useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    React.useEffect(() => {
        scrollToBottom();
    }, [chatMessages, explanation]);

    const handleSend = () => {
        if (!input.trim()) return;
        onSendMessage(input);
        setInput("");
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="tutor-panel">
            <div className="tutor-header">
                <h3>✨ AI Tutor</h3>
                <button className="close-btn" onClick={onClose}>×</button>
            </div>

            <div className="tutor-content">
                {originalText && (
                    <div className="tutor-original-text">
                        <h4>Original Text</h4>
                        <p>{originalText}</p>
                    </div>
                )}

                {loading && (
                    <div className="tutor-loading">
                        <div className="loading-spinner"></div>
                        <p>Analyzing context, grammar, and culture...</p>
                    </div>
                )}

                {error && (
                    <div className="tutor-error">
                        <p>{error}</p>
                    </div>
                )}

                {/* Explanation Section (Always shown at top of chat sort of) */}
                {explanation && !loading && (
                    <div className="explanation-container">
                        <div className="explanation-section">
                            <h4>Summary</h4>
                            <p>{explanation.summary}</p>
                        </div>

                        <div className="explanation-section">
                            <h4>Grammar Notes</h4>
                            <p>{explanation.grammar_notes}</p>
                        </div>

                        <div className="explanation-section">
                            <h4>Cultural Context</h4>
                            <p>{explanation.cultural_notes}</p>
                        </div>
                        <hr className="divider" />
                    </div>
                )}

                {/* Chat History */}
                <div className="chat-history">
                    {chatMessages.map((msg, idx) => (
                        <div key={idx} className={`chat-message ${msg.role}`}>
                            <div className="message-content">
                                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                        </div>
                    ))}
                    {isChatLoading && (
                        <div className="chat-message assistant">
                            <div className="message-content typing">...</div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {!explanation && !loading && !error && chatMessages.length === 0 && (
                    <div className="tutor-empty">
                        <p>Select a sentence to start chatting.</p>
                    </div>
                )}
            </div>

            {/* Chat Input */}
            <div className="chat-input-area">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a follow-up question..."
                    disabled={loading || isChatLoading}
                    className="chat-textarea"
                />
                <button
                    onClick={handleSend}
                    disabled={!input.trim() || loading || isChatLoading}
                    className="send-btn"
                >
                    ➤
                </button>
            </div>
        </div>
    );
};

export default TutorPanel;
