
import React, { useState, useEffect } from 'react';
import * as Popover from '@radix-ui/react-popover';
import { api, VocabularyItem } from '../services/api';
import './SelectionMenu.css';

interface SelectionMenuProps {
    selectedText: string;
    context: string;
    targetLanguage: string;
    position: { x: number; y: number } | null;
    onClose: () => void;
}

const SelectionMenu: React.FC<SelectionMenuProps> = ({ selectedText, context, targetLanguage, position, onClose }) => {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState<VocabularyItem | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Reset state when selection changes
    useEffect(() => {
        setData(null);
        setError(null);
        setLoading(false);
    }, [selectedText]);

    const handleLookup = async () => {
        setLoading(true);
        setError(null);
        try {
            const result = await api.lookupWord(selectedText, context, targetLanguage);
            setData(result);
        } catch (err) {
            console.error(err);
            setError("Failed to load definition.");
        } finally {
            setLoading(false);
        }
    };

    if (!position) return null;

    return (
        <Popover.Root open={true} onOpenChange={(open) => !open && onClose()}>
            <Popover.Anchor
                style={{
                    position: 'fixed',
                    top: position.y,
                    left: position.x,
                    width: 1,
                    height: 1,
                    visibility: 'hidden'
                }}
            />

            <Popover.Portal>
                <Popover.Content
                    className="SelectionMenuContent"
                    side="top"
                    align="center"
                    sideOffset={5}
                    onInteractOutside={onClose}
                >
                    <div className="selection-card">
                        {!data && !loading && !error && (
                            <button className="lookup-btn" onClick={handleLookup}>
                                🔍 Look up "{selectedText}"
                            </button>
                        )}

                        {loading && <div className="menu-loading">Thinking... 🧠</div>}

                        {error && <div className="menu-error">❌ {error}</div>}

                        {data && (
                            <div className="menu-result">
                                <div className="menu-header">
                                    <span className="word-title">{data.word}</span>
                                    {data.pronunciation && <span className="word-pronunciation">[{data.pronunciation}]</span>}
                                </div>
                                <div className="definition-row">
                                    <span className="value">{data.definition}</span>
                                </div>
                                <div className="translation-row">
                                    <span className="value success-text">{data.translation}</span>
                                </div>
                            </div>
                        )}
                        <Popover.Arrow className="SelectionMenuArrow" />
                    </div>
                </Popover.Content>
            </Popover.Portal>
        </Popover.Root>
    );
};

export default SelectionMenu;
