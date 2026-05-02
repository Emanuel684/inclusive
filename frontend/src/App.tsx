import { NavLink, Navigate, Route, Routes } from 'react-router-dom'
import { TextToSignPage } from './pages/TextToSignPage'
import { ImageToSignPage } from './pages/ImageToSignPage'
import { VideoToTextPage } from './pages/VideoToTextPage'

function App() {
  return (
    <main className="app-shell">
      <header>
        <h1>Inclusive Sign Translator</h1>
        <p>Traduce texto, imagen o video de señas con un flujo unificado.</p>
        <nav className="nav-tabs">
          <NavLink to="/text-to-sign">Texto a señas</NavLink>
          <NavLink to="/image-to-sign">Imagen a señas</NavLink>
          <NavLink to="/video-sign-to-text">Video señas a texto</NavLink>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Navigate to="/text-to-sign" replace />} />
        <Route path="/text-to-sign" element={<TextToSignPage />} />
        <Route path="/image-to-sign" element={<ImageToSignPage />} />
        <Route path="/video-sign-to-text" element={<VideoToTextPage />} />
      </Routes>
    </main>
  )
}

export default App
