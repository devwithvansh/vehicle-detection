import { Save } from 'lucide-react'
import { useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { api } from '../api/client'
import { toast } from '../utils/toast'

export default function RegisterVehicle() {
  const [params] = useSearchParams()
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

  async function submit(event) {
    event.preventDefault()
    if (!form.vehicle_number.trim()) {
      toast('Vehicle number is required.')
      return
    }
    try {
      await api.post('/vehicles', form)
      toast('Vehicle registered successfully.')
      setForm({
        vehicle_number: '',
        driver_name: '',
        unit_name: '',
        vehicle_type: '',
        purpose: '',
        remarks: '',
        operator_name: ''
      })
    } catch (err) {
      const detail = err.response?.data?.detail || 'Check duplicate vehicle number or required fields.'
      toast('Registration failed. ' + detail)
    }
  }

  return (
    <div className="space-y-6">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-moss">Registration</p>
        <h1 className="mt-2 text-3xl font-black">Register Vehicle</h1>
      </header>
      <form onSubmit={submit} className="glass grid gap-4 rounded-lg p-5 md:grid-cols-2">
        {Object.entries(form).map(([key, value]) => (
          <label key={key} className={key === 'remarks' ? 'md:col-span-2' : ''}>
            <span className="mb-2 block text-sm capitalize text-white/60">{key.replaceAll('_', ' ')}</span>
            {key === 'remarks' ? (
              <textarea className="input min-h-28" value={value} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />
            ) : (
              <input className="input" value={value} onChange={(e) => setForm({ ...form, [key]: e.target.value })} required={key !== 'remarks'} />
            )}
          </label>
        ))}
        <button className="btn btn-primary md:col-span-2"><Save size={18} /> Save Vehicle</button>
      </form>
    </div>
  )
}
