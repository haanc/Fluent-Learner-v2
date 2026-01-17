import { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import './DepsSetup.css'

interface DependencyStatus {
  name: string
  available: boolean
  path?: string
}

interface DownloadProgress {
  dependency: string
  status: 'checking' | 'downloading' | 'extracting' | 'done' | 'error'
  percent?: number
  message?: string
}

// Check if we're in Electron environment
const isElectron = typeof window !== 'undefined' && window.ipcRenderer

const DEP_INFO: Record<string, { icon: string; desc: string }> = {
  'yt-dlp': {
    icon: '📹',
    desc: 'Video download and streaming',
  },
  FFmpeg: {
    icon: '🎵',
    desc: 'Audio extraction and processing',
  },
}

export function DepsSetup({ onComplete }: { onComplete: () => void }) {
  const { t } = useTranslation()
  const [deps, setDeps] = useState<DependencyStatus[]>([])
  const [downloading, setDownloading] = useState(false)
  const [progress, setProgress] = useState<Record<string, DownloadProgress>>({})
  const [error, setError] = useState<string | null>(null)

  // Check dependencies on mount
  useEffect(() => {
    if (!isElectron) {
      onComplete()
      return
    }

    checkDeps()
  }, [])

  // Listen for download progress
  useEffect(() => {
    if (!isElectron) return

    const handler = (_event: any, data: DownloadProgress) => {
      setProgress((prev) => ({
        ...prev,
        [data.dependency]: data,
      }))

      // If all done, refresh deps
      if (data.status === 'done') {
        checkDeps()
      }
    }

    window.ipcRenderer.on('dependency-download-progress', handler)
    return () => {
      window.ipcRenderer.off('dependency-download-progress', handler)
    }
  }, [])

  async function checkDeps() {
    if (!isElectron) return

    try {
      const result = await window.ipcRenderer.invoke('check-dependencies')
      setDeps(result)

      // If all available, auto-complete
      if (result.every((d: DependencyStatus) => d.available)) {
        onComplete()
      }
    } catch (e) {
      console.error('Failed to check dependencies:', e)
    }
  }

  async function handleDownload() {
    if (!isElectron) return

    setDownloading(true)
    setError(null)

    try {
      const result = await window.ipcRenderer.invoke('download-dependencies')
      if (result.success) {
        await checkDeps()
      } else {
        setError(result.error || 'Download failed')
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Download failed')
    } finally {
      setDownloading(false)
    }
  }

  function handleSkip() {
    onComplete()
  }

  const missingDeps = deps.filter((d) => !d.available)
  const allAvailable = missingDeps.length === 0

  if (!isElectron || deps.length === 0) {
    return null
  }

  if (allAvailable) {
    return null
  }

  return (
    <div className="deps-setup-overlay">
      <div className="deps-setup-modal">
        <div className="deps-setup-header">
          <div className="deps-setup-icon">⚙️</div>
          <h2>{t('deps.title', 'First-Time Setup')}</h2>
          <p>{t('deps.subtitle', 'Some components need to be installed for full functionality')}</p>
        </div>

        <div className="deps-list">
          {deps.map((dep) => {
            const info = DEP_INFO[dep.name] || { icon: '📦', desc: 'Required component' }
            const prog = progress[dep.name]
            const isDownloading = prog?.status === 'downloading'
            const isExtracting = prog?.status === 'extracting'

            return (
              <div key={dep.name} className="dep-item">
                <div className="dep-icon">{info.icon}</div>
                <div className="dep-info">
                  <div className="dep-name">{dep.name}</div>
                  <div className="dep-desc">{info.desc}</div>
                </div>
                <div
                  className={`dep-status ${
                    dep.available
                      ? 'available'
                      : isDownloading || isExtracting
                        ? 'downloading'
                        : prog?.status === 'error'
                          ? 'error'
                          : 'missing'
                  }`}
                >
                  {dep.available ? (
                    <>✓ {t('deps.ready', 'Ready')}</>
                  ) : isDownloading ? (
                    <>
                      <div className="progress-bar">
                        <div className="progress-fill" style={{ width: `${prog.percent || 0}%` }} />
                      </div>
                      <span>{prog.percent}%</span>
                    </>
                  ) : isExtracting ? (
                    <>
                      <span className="spinner" />
                      {t('deps.extracting', 'Extracting...')}
                    </>
                  ) : prog?.status === 'error' ? (
                    <>{t('deps.error', 'Error')}</>
                  ) : (
                    <>{t('deps.missing', 'Missing')}</>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {error && <div className="deps-error" style={{ color: '#f87171', textAlign: 'center', marginBottom: 16 }}>{error}</div>}

        <div className="deps-actions">
          <button className="deps-btn deps-btn-secondary" onClick={handleSkip} disabled={downloading}>
            {t('deps.skip', 'Skip for now')}
          </button>
          <button className="deps-btn deps-btn-primary" onClick={handleDownload} disabled={downloading}>
            {downloading ? (
              <>
                <span className="spinner" style={{ marginRight: 8 }} />
                {t('deps.downloading', 'Downloading...')}
              </>
            ) : (
              t('deps.install', 'Install Components')
            )}
          </button>
        </div>

        <div className="deps-note">
          {t('deps.note', 'Components will be stored in app data folder (~100MB)')}
        </div>
      </div>
    </div>
  )
}
