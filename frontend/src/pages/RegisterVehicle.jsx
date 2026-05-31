import { Save, UserPlus, Info, ArrowLeft } from 'lucide-react'
import { useMemo, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { toast } from '../utils/toast'

export default function RegisterVehicle() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const initial = useMemo(() => params.get('vehicle_number') || '', [params])
  
  const [form, setForm] = useState({
    vehicle_number: initial,
    driver_name: '',
    unit_name: '',
    vehicle_type: '',
    purpose: '',
    remarks: '',
    operator_name: ''
  })
  const [busy, setBusy] = useState(false)

  async function submit(event) {
    event.preventDefault()
    if (!form.vehicle_number.trim()) {
      toast('Vehicle number is required.')
      return
    }
    
    setBusy(true)
    try {
      await api.post('/vehicles', form)
      toast('Vehicle registered successfully.')
      // Instead of just resetting, let's redirect to detection or list
      setTimeout(() => navigate('/camera'), 1000)
    } catch (err) {
      const detail = err.response?.data?.detail || 'Check duplicate vehicle number or required fields.'
      toast('Registration failed. ' + detail)
    } finally {
      setBusy(false)
    }
  }

  const fields = [
    { key: 'vehicle_number', label: 'Plate Number', placeholder: 'e.g. 21B123456K', icon: 'ID' },
    { key: 'driver_name', label: 'Driver Name', placeholder: 'Rank & Name' },
    { key: 'unit_name', label: 'Unit / Regiment', placeholder: 'e.g. 15 Rajput' },
    { key: 'vehicle_type', label: 'Vehicle Type', placeholder: 'e.g. Gypsy, Stallion' },
    { key: 'purpose', label: 'Purpose of Entry', placeholder: 'e.g. Maintenance, Convoy' },
    { key: 'operator_name', label: 'Authorized By', placeholder: 'Officer Name' },
    { key: 'remarks', label: 'Additional Remarks', placeholder: 'Any other details...', fullWidth: true },
  ]

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center gap-1 text-xs font-bold text-white/40 hover:text-moss transition-colors mb-2 uppercase tracking-widest"
          >
            <ArrowLeft size={14} /> Back
          </button>
          <h1 className="text-3xl font-black text-white flex items-center gap-3">
            <UserPlus className="text-moss" size={32} /> New Registration
          </h1>
        </div>
        <div className="hidden md:flex items-center gap-3 bg-moss/10 border border-moss/20 p-3 rounded-xl">
          <Info className="text-moss" size={20} />
          <p className="text-[10px] leading-tight text-moss/80 font-bold uppercase tracking-tighter">
            Registering a new vehicle<br/>into the secure log system.
          </p>
        </div>
      </header>

      <form onSubmit={submit} className="bg-white/5 border border-white/10 rounded-2xl p-8 shadow-2xl backdrop-blur-md">
        <div className="grid gap-6 md:grid-cols-2">
          {fields.map((f) => (
            <label key={f.key} className={`${f.fullWidth ? 'md:col-span-2' : ''} group`}>
              <span className="mb-2 block text-xs font-black uppercase tracking-widest text-white/40 group-focus-within:text-moss transition-colors">
                {f.label}
              </span>
              {f.key === 'remarks' ? (
                <textarea 
                  className="w-full bg-white/[0.03] border border-white/10 rounded-xl p-4 text-white focus:outline-none focus:border-moss/50 focus:bg-moss/5 transition-all min-h-32 resize-none placeholder:text-white/10"
                  value={form[f.key]} 
                  placeholder={f.placeholder}
                  onChange={(e) => setForm({ ...form, [f.key]: e.target.value })} 
                />
              ) : (
                <input 
                  className="w-full bg-white/[0.03] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-moss/50 focus:bg-moss/5 transition-all placeholder:text-white/10 font-medium"
                  value={form[f.key]} 
                  placeholder={f.placeholder}
                  onChange={(e) => setForm({ ...form, [f.key]: e.target.value })} 
                  required={f.key !== 'remarks'}
                />
              )}
            </label>
          ))}
        </div>

        <div className="mt-8 pt-8 border-t border-white/5 flex flex-col md:flex-row gap-4 items-center justify-between">
          <p className="text-xs text-white/30 italic font-medium">
            * All fields except remarks are mandatory for security compliance.
          </p>
          <button 
            disabled={busy}
            className="w-full md:w-auto flex items-center justify-center gap-3 px-10 py-4 bg-moss text-black font-black rounded-xl hover:bg-moss/90 transition-all active:scale-95 disabled:opacity-50 shadow-[0_10px_20px_rgba(130,150,80,0.2)]"
          >
            {busy ? (
              <div className="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <><Save size={20} /> COMPLETE REGISTRATION</>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
