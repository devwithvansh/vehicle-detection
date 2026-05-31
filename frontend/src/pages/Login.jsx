import { Lock, ShieldCheck, User, LogIn } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { toast } from '../utils/toast'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ username: 'admin', password: 'Admin@12345' })
  const [busy, setBusy] = useState(false)

  async function submit(event) {
    event.preventDefault()
    if (!form.username.trim() || !form.password.trim()) {
      toast('Username and password are required.')
      return
    }
    setBusy(true)
    try {
      await login(form.username, form.password)
      navigate('/')
    } catch {
      toast('Access denied. Check credentials.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#080b08] flex items-center justify-center px-4 text-white relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 right-0 w-96 h-96 bg-moss rounded-full blur-3xl opacity-10"></div>
        <div className="absolute bottom-0 left-0 w-96 h-96 bg-moss rounded-full blur-3xl opacity-10"></div>
      </div>

      <form onSubmit={submit} className="relative w-full max-w-md">
        {/* Card Container */}
        <div className="bg-white/[0.03] border border-white/10 backdrop-blur-xl rounded-2xl p-10 shadow-2xl">
          {/* Header */}
          <div className="mb-10 flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-moss/20 border border-moss/30 shadow-lg shadow-moss/10">
              <ShieldCheck size={28} className="text-moss" />
            </div>
            <div>
              <p className="text-[10px] uppercase tracking-[0.3em] text-moss/80 font-black">Secure Access</p>
              <h1 className="text-2xl font-black text-white tracking-tight">ARMOR<span className="text-moss">SCAN</span></h1>
            </div>
          </div>

          {/* Form Fields */}
          <div className="space-y-5 mb-8">
            <label className="block group">
              <span className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-widest text-white/40 group-focus-within:text-moss transition-colors">
                <User size={14} /> Username
              </span>
              <input 
                className="w-full bg-white/[0.03] border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-moss/50 focus:bg-moss/[0.02] transition-all placeholder:text-white/10 font-medium"
                placeholder="Enter your username"
                value={form.username} 
                onChange={(e) => setForm({ ...form, username: e.target.value })} 
              />
            </label>
            
            <label className="block group">
              <span className="mb-2 flex items-center gap-2 text-xs font-black uppercase tracking-widest text-white/40 group-focus-within:text-moss transition-colors">
                <Lock size={14} /> Password
              </span>
              <input 
                className="w-full bg-white/[0.03] border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-moss/50 focus:bg-moss/[0.02] transition-all placeholder:text-white/10 font-medium"
                type="password" 
                placeholder="Enter your password"
                value={form.password} 
                onChange={(e) => setForm({ ...form, password: e.target.value })} 
              />
            </label>
          </div>

          {/* Submit Button */}
          <button 
            className="w-full flex items-center justify-center gap-3 py-4 bg-moss text-black font-black rounded-lg hover:bg-moss/90 transition-all active:scale-95 disabled:opacity-50 shadow-[0_10px_20px_rgba(139,155,79,0.2)]"
            disabled={busy}
          >
            {busy ? (
              <>
                <div className="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
                AUTHENTICATING...
              </>
            ) : (
              <>
                <LogIn size={20} /> ENTER SYSTEM
              </>
            )}
          </button>

          {/* Footer Info */}
          <p className="text-center text-[10px] text-white/30 uppercase tracking-widest font-bold mt-6">
            Restricted Military Access<br/>Unauthorized access prohibited
          </p>
        </div>
      </form>
    </div>
  )
}
