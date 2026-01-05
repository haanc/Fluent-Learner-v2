
import React from 'react';
import './SubtitleOverlay.css';

interface SubtitleOverlayProps {
    text: string | null;
}

const SubtitleOverlay: React.FC<SubtitleOverlayProps> = ({ text }) => {
    if (!text) return null;

    return (
        <div className="subtitle-overlay">
            <p>{text}</p>
        </div>
    );
};

export default SubtitleOverlay;
