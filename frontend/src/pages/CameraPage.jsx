import { Camera, ImageUp, ScanLine } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { toast } from '../utils/toast'

export default function CameraPage() {
  const videoRef = useRef(null)
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [cameras, setCameras] = useState([])
  const [history, setHistory] = useState([])
  const [cameraLocationId, setCameraLocationId] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/cameras').then((res) => {
      setCameras(res.data)
      if (res.data[0]) setCameraLocationId(String(res.data[0].id))
    })
    api.get('/ocr/history').then((res) => setHistory(res.data))
    navigator.mediaDevices?.getUserMedia({ video: true }).then((stream) => {
      if (videoRef.current) videoRef.current.srcObject = stream
    }).catch(() => toast('Camera preview unavailable. Upload still works.'))
  }, [])

  async function captureFromVideo() {
    const video = videoRef.current
    if (!video) return
    const canvas = document.createElement('canvas')
    canvas.width = video.videoWidth || 1280
    canvas.height = video.videoHeight || 720
    canvas.getContext('2d').drawImage(video, 0, 0)
    canvas.toBlob((blob) => submit(new File([blob], 'capture.jpg', { type: 'image/jpeg' })), 'image/jpeg')
  }

  async function submit(selectedFile = file) {
    if (!selectedFile) return toast('Select or capture an image first.')
    const form = new FormData()
    form.append('image', selectedFile)
    if (cameraLocationId) form.append('camera_location_id', cameraLocationId)
    setBusy(true)
    try {
      const res = await api.post('/ocr/capture', form)
      setResult(res.data)
      api.get('/ocr/history').then((historyRes) => setHistory(historyRes.data))
      toast(res.data.message)
      
      if (!res.data.vehicle_exists) {
        const number = res.data.detected_number || ''
        // Always redirect if not exists, even if number is empty, so user can manually register
        setTimeout(() => {
          navigate(`/register?vehicle_number=${encodeURIComponent(number)}`)
        }, 1500)
      }
    } catch (err) {
      console.error(err)
      toast('OCR processing failed. ' + (err.response?.data?.detail || ''))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-moss">Detection Module</p>
        <h1 className="mt-2 text-3xl font-black">Live Camera and OCR Capture</h1>
      </header>
      <div className="grid gap-6 xl:grid-cols-[1.4fr_.8fr]">
        <div className="glass overflow-hidden rounded-lg">
          <video ref={videoRef} autoPlay playsInline muted className="aspect-video w-full bg-black object-cover" />
          <div className="flex flex-wrap gap-3 p-4">
            <button className="btn btn-primary" onClick={captureFromVideo} disabled={busy}><Camera size={18} /> Capture</button>
            <label className="btn btn-secondary cursor-pointer">
  <ImageUp size={18} /> Upload
  <input
    type="file"
    accept="image/*"
    className="hidden"
    onChange={(e) => {

      const selected = e.target.files?.[0]

      if (!selected) return

      setFile(selected)

      submit(selected)

    }}
  />
</label>
            <button className="btn btn-secondary" onClick={() => submit()} disabled={busy}><ScanLine size={18} /> Run OCR</button>
          </div>
        </div>
        <div className="space-y-6">
          <div className="glass rounded-lg p-5">
            <label className="mb-4 block">
              <span className="mb-2 block text-sm text-white/60">Camera location</span>
              <select className="input" value={cameraLocationId} onChange={(e) => setCameraLocationId(e.target.value)}>
                {cameras.map((cam) => <option key={cam.id} value={cam.id}>{cam.name}</option>)}
              </select>
            </label>
            <div className="rounded-lg border border-white/10 bg-white/[0.03] p-4">
              <p className="text-sm text-white/60">Detected number</p>
              <p className="mt-2 text-3xl font-black text-moss">{result?.detected_number || 'Awaiting scan'}</p>
              <p className="mt-3 text-sm text-white/60">Confidence: {result ? `${Math.round(result.confidence_score * 100)}%` : 'N/A'}</p>
              <p className="mt-3 text-sm text-white/60">{file?.name || 'No upload selected'}</p>
            </div>
          </div>
          <div className="glass rounded-lg p-5">
            <h2 className="mb-4 font-bold">Image History</h2>
            <div className="space-y-3">
              {history.slice(0, 6).map((item) => (
                <div key={item.id} className="rounded-lg border border-white/10 bg-white/[0.03] p-3">
                  <div className="flex justify-between gap-3">
                    <p className="font-bold text-moss">{item.detected_number || 'Unreadable'}</p>
                    <span className="text-xs text-white/50">{item.confidence_score ? `${Math.round(item.confidence_score * 100)}%` : 'N/A'}</span>
                  </div>
                  <p className="mt-1 truncate text-xs text-white/45">{item.original_path}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
