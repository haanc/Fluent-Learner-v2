
import React, { useState } from 'react';
import { X, Mail, Lock, LogIn, UserPlus } from 'lucide-react';
import { signIn, signUp } from '../../services/supabase';

interface AuthModalProps {
    isOpen: boolean;
    onClose: () => void;
    onLoginSuccess: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onLoginSuccess }) => {
    const [mode, setMode] = useState<'login' | 'signup'>('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            if (mode === 'login') {
                const { error } = await signIn(email, password);
                if (error) throw error;
                onLoginSuccess();
                onClose();
            } else {
                const { error } = await signUp(email, password);
                if (error) throw error;
                alert('Sign up successful! Please check your email for confirmation.');
                setMode('login'); // Switch to login after signup
            }
        } catch (err: any) {
            setError(err.message || 'Authentication failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-overlay" style={{
            position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
            background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(5px)',
            display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 2000
        }}>
            <div className="auth-modal" style={{
                background: '#1e1e24', width: '400px', borderRadius: '16px',
                padding: '32px', border: '1px solid rgba(255,255,255,0.1)',
                boxShadow: '0 20px 50px rgba(0,0,0,0.5)', position: 'relative'
            }}>
                <button onClick={onClose} style={{
                    position: 'absolute', top: '16px', right: '16px',
                    background: 'transparent', border: 'none', color: '#64748b', cursor: 'pointer'
                }}>
                    <X size={20} />
                </button>

                <h2 style={{
                    fontSize: '1.8rem', fontWeight: 800, marginBottom: '24px', textAlign: 'center',
                    background: 'linear-gradient(135deg, #fff 0%, #cbd5e1 100%)',
                    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'
                }}>
                    {mode === 'login' ? 'Welcome Back' : 'Create Account'}
                </h2>

                <div className="auth-tabs" style={{ display: 'flex', gap: '8px', marginBottom: '24px', background: 'rgba(255,255,255,0.05)', padding: '4px', borderRadius: '12px' }}>
                    <button
                        onClick={() => setMode('login')}
                        style={{
                            flex: 1, padding: '10px', borderRadius: '8px', border: 'none', cursor: 'pointer',
                            background: mode === 'login' ? '#6366f1' : 'transparent',
                            color: mode === 'login' ? '#fff' : '#94a3b8', fontWeight: 600,
                            transition: 'all 0.2s', outline: 'none'
                        }}
                    >
                        Login
                    </button>
                    <button
                        onClick={() => setMode('signup')}
                        style={{
                            flex: 1, padding: '10px', borderRadius: '8px', border: 'none', cursor: 'pointer',
                            background: mode === 'signup' ? '#6366f1' : 'transparent',
                            color: mode === 'signup' ? '#fff' : '#94a3b8', fontWeight: 600,
                            transition: 'all 0.2s', outline: 'none'
                        }}
                    >
                        Sign Up
                    </button>
                </div>

                {error && (
                    <div style={{
                        background: 'rgba(239, 68, 68, 0.15)', color: '#fca5a5', border: '1px solid rgba(239, 68, 68, 0.2)',
                        padding: '12px', borderRadius: '8px', marginBottom: '16px', fontSize: '0.9rem', display: 'flex', alignItems: 'center'
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                    <div className="input-group">
                        <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.85rem', marginBottom: '8px', fontWeight: 500 }}>Email</label>
                        <div style={{ position: 'relative' }}>
                            <Mail size={18} style={{ position: 'absolute', left: '14px', top: '14px', color: '#94a3b8' }} />
                            <input
                                type="email"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                required
                                style={{
                                    width: '100%', padding: '14px 14px 14px 44px',
                                    background: 'rgba(0, 0, 0, 0.2)', border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '10px', color: '#fff', outline: 'none',
                                    transition: 'border-color 0.2s, background 0.2s',
                                    fontSize: '0.95rem',
                                    boxSizing: 'border-box' // Fix overflow
                                }}
                                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                                onBlur={(e) => e.target.style.borderColor = 'rgba(255, 255, 255, 0.1)'}
                                placeholder="name@example.com"
                            />
                        </div>
                    </div>

                    <div className="input-group">
                        <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.85rem', marginBottom: '8px', fontWeight: 500 }}>Password</label>
                        <div style={{ position: 'relative' }}>
                            <Lock size={18} style={{ position: 'absolute', left: '14px', top: '14px', color: '#94a3b8' }} />
                            <input
                                type="password"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                                style={{
                                    width: '100%', padding: '14px 14px 14px 44px',
                                    background: 'rgba(0, 0, 0, 0.2)', border: '1px solid rgba(255, 255, 255, 0.1)',
                                    borderRadius: '10px', color: '#fff', outline: 'none',
                                    transition: 'border-color 0.2s, background 0.2s',
                                    fontSize: '0.95rem',
                                    boxSizing: 'border-box' // Fix overflow
                                }}
                                onFocus={(e) => e.target.style.borderColor = '#6366f1'}
                                onBlur={(e) => e.target.style.borderColor = 'rgba(255, 255, 255, 0.1)'}
                                placeholder="••••••••"
                            />
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            marginTop: '12px', padding: '14px', borderRadius: '10px', border: 'none',
                            background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)',
                            color: '#fff', fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer',
                            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
                            opacity: loading ? 0.7 : 1, transition: 'transform 0.1s',
                            boxShadow: '0 4px 6px -1px rgba(99, 102, 241, 0.3)'
                        }}
                    >
                        {loading ? 'Processing...' : (
                            <>
                                {mode === 'login' ? <LogIn size={18} /> : <UserPlus size={18} />}
                                {mode === 'login' ? 'Sign In' : 'Create Account'}
                            </>
                        )}
                    </button>
                </form>
            </div>
        </div>
    );
};
