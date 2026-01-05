import { app, BrowserWindow, protocol, ipcMain, dialog } from 'electron'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import fs from 'node:fs'
import { Readable } from 'node:stream'
import { spawn, ChildProcess } from 'node:child_process'


const __dirname = path.dirname(fileURLToPath(import.meta.url))

// The built directory structure
process.env.APP_ROOT = path.join(__dirname, '..')

// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
export const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']
export const MAIN_DIST = path.join(process.env.APP_ROOT, 'dist-electron')
export const RENDERER_DIST = path.join(process.env.APP_ROOT, 'dist')

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL ? path.join(process.env.APP_ROOT, 'public') : RENDERER_DIST

let win: BrowserWindow | null
let pyProcess: ChildProcess | null = null

// Register local protocol for videos
function registerLocalProtocol() {
  protocol.handle('local-video', (request) => {
    try {
      let pathPart = request.url.slice('local-video://'.length)
      const filePath = decodeURIComponent(pathPart)

      const stat = fs.statSync(filePath)
      const fileSize = stat.size
      const range = request.headers.get('Range')

      if (range) {
        const parts = range.replace(/bytes=/, "").split("-")
        const start = parseInt(parts[0], 10)
        const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1
        const chunksize = (end - start) + 1

        const file = fs.createReadStream(filePath, { start, end })
        // @ts-ignore
        const stream = Readable.toWeb(file)

        return new Response(stream as any, {
          status: 206,
          headers: {
            'Content-Range': `bytes ${start}-${end}/${fileSize}`,
            'Content-Length': chunksize.toString(),
            'Content-Type': 'video/mp4',
            'Accept-Ranges': 'bytes'
          }
        })
      } else {
        const file = fs.createReadStream(filePath)
        // @ts-ignore
        const stream = Readable.toWeb(file)
        return new Response(stream as any, {
          status: 200,
          headers: {
            'Content-Length': fileSize.toString(),
            'Content-Type': 'video/mp4',
            'Accept-Ranges': 'bytes'
          }
        })
      }
    } catch (e) {
      console.error('Local Video Error:', e)
      return new Response('Not Found', { status: 404 })
    }
  })
}

function handleIpc() {
  ipcMain.handle('open-file-dialog', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [
        { name: 'Movies', extensions: ['mkv', 'avi', 'mp4', 'webm'] },
        { name: 'Audio', extensions: ['mp3', 'wav', 'ogg'] },
        { name: 'All Files', extensions: ['*'] }
      ]
    })
    if (canceled) return null
    return filePaths[0]
  })
}

function startPythonBackend() {
  const isDev = VITE_DEV_SERVER_URL != null

  if (isDev) {
    console.log('Dev mode detected: Skipping auto-spawn of Python backend. Please ensure backend is running manually.')
    return
  }

  const pythonPath = path.join(process.resourcesPath, 'backend', 'venv', 'Scripts', 'python.exe')
  const scriptPath = path.join(process.env.APP_ROOT, 'backend', 'main.py')

  console.log('Starting Python backend:', pythonPath, scriptPath)

  pyProcess = spawn(pythonPath, [scriptPath])

  pyProcess.stdout?.on('data', (data) => {
    console.log(`Python: ${data}`)
  })

  pyProcess.stderr?.on('data', (data) => {
    console.error(`Python Error: ${data}`)
  })

  pyProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`)
  })
}

function createWindow() {
  win = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: path.join(process.env.VITE_PUBLIC, 'electron-vite.svg'),
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
    },
  })

  // Test active push message to Renderer-process.
  win.webContents.on('did-finish-load', () => {
    win?.webContents.send('main-process-message', (new Date).toLocaleString())
  })

  if (VITE_DEV_SERVER_URL) {
    win.loadURL(VITE_DEV_SERVER_URL)
  } else {
    win.loadFile(path.join(RENDERER_DIST, 'index.html'))
  }
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
    win = null
  }
})

app.on('will-quit', () => {
  if (pyProcess) {
    console.log('Terminating Python backend...')
    pyProcess.kill()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

app.whenReady().then(() => {
  registerLocalProtocol()
  handleIpc()
  startPythonBackend()
  createWindow()
})
