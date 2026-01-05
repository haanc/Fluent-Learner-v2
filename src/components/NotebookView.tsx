import React, { useEffect, useState } from 'react';
import { api, SavedWord } from '../services/api';
import './NotebookView.css';

const LANGUAGES = ["All", "English", "French", "Spanish", "German", "Chinese", "Japanese"];

const NotebookView: React.FC = () => {
    const [words, setWords] = useState<SavedWord[]>([]);
    const [loading, setLoading] = useState(true);
    const [mode, setMode] = useState<'list' | 'review'>('list');

    // Filters
    const [filterLanguage, setFilterLanguage] = useState('All');

    // Review State
    const [reviewQueue, setReviewQueue] = useState<SavedWord[]>([]);
    const [currentReviewIndex, setCurrentReviewIndex] = useState(0);
    const [isFlipped, setIsFlipped] = useState(false);

    const fetchWords = async () => {
        setLoading(true);
        try {
            const data = await api.listSavedWords(filterLanguage);
            setWords(data);
        } catch (e) {
            console.error("Failed to load vocab", e);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchWords();
        // Reset scroll to top of container
        const container = document.querySelector('.notebook-container');
        if (container) container.scrollTop = 0;
    }, [filterLanguage]);

    // Listen for global updates (e.g. from Sidebar)
    useEffect(() => {
        const handleRefresh = () => fetchWords();
        window.addEventListener('vocab-updated', handleRefresh);
        return () => window.removeEventListener('vocab-updated', handleRefresh);
    }, []);

    const startReview = async () => {
        setLoading(true);
        try {
            // Fetch ONLY due words for the selected language
            const dueWords = await api.listSavedWords(filterLanguage, true);
            setReviewQueue(dueWords);
            setCurrentReviewIndex(0);
            setIsFlipped(false);
            if (dueWords.length > 0) {
                setMode('review');
            } else {
                alert("No words due for review!");
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const handleReviewAction = async (quality: number) => {
        const currentWord = reviewQueue[currentReviewIndex];
        if (!currentWord) return;

        // Optimistic UI update could happen here, but for safety await backend
        try {
            await api.reviewWord(currentWord.id, quality);

            // Move to next card
            setIsFlipped(false);
            if (currentReviewIndex + 1 < reviewQueue.length) {
                setCurrentReviewIndex(prev => prev + 1);
            } else {
                alert("Review Session Complete! 🎉");
                setMode('list');
                fetchWords(); // Refresh list
            }
        } catch (e) {
            alert("Failed to submit review");
        }
    };

    const handleDelete = async (id: string) => {
        if (confirm('Delete this word?')) {
            await api.deleteSavedWord(id);
            setWords(words.filter(w => w.id !== id));
        }
    };

    // --- RENDER HELPERS ---

    const renderReviewCard = () => {
        const word = reviewQueue[currentReviewIndex];
        if (!word) return null;

        return (
            <div className="review-container">
                <div className="review-header">
                    <button className="back-btn" onClick={() => setMode('list')}>← Exit Review</button>
                    <span>{currentReviewIndex + 1} / {reviewQueue.length}</span>
                </div>

                <div className={`flashcard ${isFlipped ? 'flipped' : ''}`} onClick={() => setIsFlipped(!isFlipped)}>
                    <div className="card-front">
                        <h2>{word.word}</h2>
                        {word.context_sentence && <p className="context">"{word.context_sentence}"</p>}
                        <p className="hint">(Click to flip)</p>
                    </div>
                    <div className="card-back">
                        <h2>{word.word}</h2>
                        <div className="def-section">
                            <label>Translation:</label>
                            <p>{word.translation || "No translation"}</p>
                        </div>
                        {/* Show more details if stored, like definition */}
                    </div>
                </div>

                {isFlipped && (
                    <div className="review-actions">
                        <button className="rate-btn again" onClick={() => handleReviewAction(0)}>
                            Again (1m)
                        </button>
                        <button className="rate-btn hard" onClick={() => handleReviewAction(3)}>
                            Hard (2d)
                        </button>
                        <button className="rate-btn good" onClick={() => handleReviewAction(4)}>
                            Good (4d)
                        </button>
                        <button className="rate-btn easy" onClick={() => handleReviewAction(5)}>
                            Easy (7d)
                        </button>
                    </div>
                )}
            </div>
        );
    };

    return (
        <div className="notebook-container">
            {mode === 'review' ? renderReviewCard() : (
                <>
                    <div className="notebook-header">
                        <h2>📚 Smart Vocabulary Notebook</h2>
                        <div className="notebook-controls">
                            <select
                                value={filterLanguage}
                                onChange={(e) => setFilterLanguage(e.target.value)}
                                className="lang-filter"
                            >
                                {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
                            </select>
                            <button className="review-btn" onClick={startReview}>
                                ▶ Start Review
                            </button>
                        </div>
                    </div>

                    {loading ? (
                        <p>Loading...</p>
                    ) : (
                        <div className="vocab-grid">
                            {words.length === 0 && <p className="empty-state">No words found.</p>}
                            {words.map(w => (
                                <div key={w.id} className="vocab-card">
                                    <div className="vocab-word-row">
                                        <div className="word-info">
                                            <span className="vocab-word">{w.word}</span>
                                            {w.language && <span className="lang-tag">{w.language}</span>}
                                        </div>
                                        <button className="delete-btn" onClick={() => handleDelete(w.id)}>×</button>
                                    </div>
                                    {w.translation && <div className="vocab-trans">{w.translation}</div>}
                                    {w.context_sentence && (
                                        <div className="vocab-context">"{w.context_sentence}"</div>
                                    )}
                                    <div className="vocab-meta">
                                        Next Review: {new Date(w.next_review_at || w.created_at).toLocaleDateString()}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default NotebookView;
