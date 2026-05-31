import { Camera, ImageUp, ScanLine, UserPlus, History } from 'lucide-react'
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
    // Parallelize initial data fetching
    Promise.all([
      api.get('/cameras').catch(() => ({ data: [] })),
      api.get('/ocr/history').catch(() => ({ data: [] }))
    ]).then(([camRes, histRes]) => {
      setCameras(camRes.data)
      if (camRes.data[0]) setCameraLocationId(String(camRes.data[0].id))
      setHistory(histRes.data)
    })

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
    canvas.toBlob((blob) => submit(new File([blob], `capture_${Date.now()}.jpg`, { type: 'image/jpeg' })), 'image/jpeg')
  }

  async function submit(selectedFile = file) {
    if (!selectedFile) return toast('Select or capture an image first.')
    
    const form = new FormData()
    form.append('image', selectedFile)
    if (cameraLocationId) form.append('camera_location_id', cameraLocationId)
    
    setBusy(true)
    setResult(null) // Reset previous result

    try {
      const res = await api.post('/ocr/capture', form)
      setResult(res.data)
      
      // Refresh history in background
      api.get('/ocr/history').then((historyRes) => setHistory(historyRes.data))
      
      toast(res.data.message)
      
      // Improved logic: Don't auto-redirect. Let the user decide.
      // If the vehicle doesn't exist, show a prominent "Register" button instead.
    } catch (err) {
      console.error(err)
      toast('OCR processing failed. ' + (err.response?.data?.detail || ''))
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-moss font-bold">Detection Module</p>
          <h1 className="mt-1 text-3xl font-black text-white">Vehicle Scanner</h1>
        </div>
        <div className="flex items-center gap-2 bg-white/5 p-2 rounded-lg border border-white/10">
          <span className="text-xs text-white/40 uppercase font-medium px-2">Location:</span>
          <select 
            className="bg-transparent text-sm font-bold text-moss focus:outline-none cursor-pointer" 
            value={cameraLocationId} 
            onChange={(e) => setCameraLocationId(e.target.value)}
          >
            {cameras.map((cam) => <option key={cam.id} value={cam.id} className="bg-[#1a1c1e]">{cam.name}</option>)}
          </select>
        </div>
      </header>

      <div className="grid gap-6 xl:grid-cols-[1fr_400px]">
        <div className="flex flex-col gap-4">
          <div className="relative aspect-video w-full bg-black rounded-xl overflow-hidden border border-white/10 shadow-2xl">
            <video ref={videoRef} autoPlay playsInline muted className="h-full w-full object-cover" />
            {busy && (
              <div className="absolute inset-0 bg-black/60 flex flex-col items-center justify-center backdrop-blur-sm">
                <div className="w-12 h-12 border-4 border-moss border-t-transparent rounded-full animate-spin mb-4"></div>
                <p className="text-moss font-bold tracking-widest animate-pulse">ANALYZING PLATE...</p>
              </div>
            )}
            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex gap-4">
               <button 
                className="flex items-center gap-2 px-6 py-3 bg-moss text-black font-black rounded-full hover:bg-moss/90 transition-all active:scale-95 shadow-lg disabled:opacity-50" 
                onClick={captureFromVideo} 
                disabled={busy}
              >
                <Camera size={20} /> SCAN NOW
              </button>
            </div>
          </div>

          <div className="flex gap-3">
            <label className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-white/5 border border-white/10 text-white font-bold rounded-lg hover:bg-white/10 transition-all cursor-pointer">
              <ImageUp size={18} /> UPLOAD IMAGE
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
            <button 
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-white/5 border border-white/10 text-white font-bold rounded-lg hover:bg-white/10 transition-all disabled:opacity-50" 
              onClick={() => submit()} 
              disabled={busy || !file}
            >
              <ScanLine size={18} /> RETRY OCR
            </button>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          {/* Scan Result Card */}
          <div className={`p-6 rounded-xl border transition-all ${result ? 'bg-moss/10 border-moss/30 shadow-[0_0_20px_rgba(130,150,80,0.1)]' : 'bg-white/5 border-white/10'}`}>
            <h2 className="text-xs uppercase tracking-widest text-white/40 font-bold mb-4">Scan Result</h2>
            
            {result ? (
              <div className="space-y-4">
                <div>
                  <p className="text-xs text-white/40 uppercase font-medium">Detected Number</p>
                  <p className="text-4xl font-black text-moss tracking-tighter mt-1">{result.detected_number || 'UNKNOWN'}</p>
                </div>
                
                <div className="flex justify-between items-end">
                  <div>
                    <p className="text-xs text-white/40 uppercase font-medium">Confidence</p>
                    <p className="text-lg font-bold text-white">{Math.round(result.confidence_score * 100)}%</p>
                  </div>
                  <div className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter ${result.vehicle_exists ? 'bg-green-500/20 text-green-400' : 'bg-amber-500/20 text-amber-400'}`}>
                    {result.vehicle_exists ? 'Registered' : 'New Vehicle'}
                  </div>
                </div>

                {!result.vehicle_exists && (
                  <button 
                    onClick={() => navigate(`/register?vehicle_number=${encodeURIComponent(result.detected_number || '')}`)}
                    className="w-full flex items-center justify-center gap-2 py-3 bg-moss text-black font-black rounded-lg hover:bg-moss/90 transition-all mt-2"
                  >
                    <UserPlus size={18} /> REGISTER VEHICLE
                  </button>
                )}
                
                <p className="text-sm text-white/60 italic leading-tight border-t border-white/10 pt-3 mt-3">{result.message}</p>
              </div>
            ) : (
              <div className="py-12 flex flex-col items-center justify-center text-center opacity-30">
                <ScanLine size={48} className="mb-4" />
                <p className="font-bold uppercase tracking-widest text-sm">Ready to scan</p>
              </div>
            )}
          </div>

          {/* Recent History Card */}
          <div className="bg-white/5 border border-white/10 rounded-xl p-6 flex-1 overflow-hidden flex flex-col">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xs uppercase tracking-widest text-white/40 font-bold flex items-center gap-2">
                <History size={14} /> Recent Scans
              </h2>
            </div>
            
            <div className="space-y-3 overflow-y-auto pr-2">
              {history.length > 0 ? history.slice(0, 5).map((item) => (
                <div key={item.id} className="p-3 rounded-lg bg-white/[0.03] border border-white/5 hover:border-white/20 transition-all group">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="font-black text-moss text-lg tracking-tight leading-none">{item.detected_number || '???'}</p>
                      <p className="text-[10px] text-white/30 uppercase mt-1 font-bold">
                        {new Date(item.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                    <span className="text-[10px] font-bold text-white/40 bg-white/5 px-2 py-0.5 rounded">
                      {Math.round(item.confidence_score * 100)}%
                    </span>
                  </div>
                </div>
              )) : (
                <p className="text-center py-8 text-sm text-white/20 italic font-medium">No scan history yet</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
