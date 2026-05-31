import { Lock, ShieldCheck, User } from 'lucide-react'
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
    <div className="grid min-h-screen place-items-center px-4 text-white">
      <form onSubmit={submit} className="glass w-full max-w-md rounded-xl p-8 shadow-tactical">
        <div className="mb-8 flex items-center gap-3">
          <div className="grid h-12 w-12 place-items-center rounded-lg bg-moss text-bunker">
            <ShieldCheck size={26} />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.28em] text-moss">Restricted Access</p>
            <h1 className="text-2xl font-black">Vehicle Sentinel</h1>
          </div>
        </div>
        <label className="mb-4 block">
          <span className="mb-2 flex items-center gap-2 text-sm text-white/70"><User size={16} /> Username</span>
          <input className="input" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
        </label>
        <label className="mb-6 block">
          <span className="mb-2 flex items-center gap-2 text-sm text-white/70"><Lock size={16} /> Password</span>
          <input className="input" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
        </label>
        <button className="btn btn-primary w-full" disabled={busy}>{busy ? 'Authenticating...' : 'Enter Command Console'}</button>
      </form>
    </div>
  )
}
