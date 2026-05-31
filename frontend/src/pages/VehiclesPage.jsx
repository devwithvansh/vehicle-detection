import { Search } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'

export default function VehiclesPage() {
  const [q, setQ] = useState('')
  const [vehicles, setVehicles] = useState([])

  useEffect(() => {
    const id = setTimeout(() => {
      api.get('/vehicles', { params: { q } }).then((res) => setVehicles(res.data))
    }, 250)
    return () => clearTimeout(id)
  }, [q])

  return (
    <div className="space-y-6">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-moss">Fleet Registry</p>
        <h1 className="mt-2 text-3xl font-black">Registered Vehicles</h1>
      </header>
      <div className="glass rounded-lg p-4">
        <div className="relative mb-4">
          <Search className="absolute left-3 top-3 text-white/40" size={18} />
          <input className="input pl-10" placeholder="Search vehicle, driver, unit, type" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[800px] text-left text-sm">
            <thead className="text-white/50">
              <tr><th className="p-3">Vehicle</th><th>Driver</th><th>Unit</th><th>Type</th><th>Purpose</th><th>Operator</th></tr>
            </thead>
            <tbody>
              {vehicles.map((item) => (
                <tr key={item.id} className="border-t border-white/10">
                  <td className="p-3 font-bold text-moss">{item.vehicle_number}</td>
                  <td>{item.driver_name}</td>
                  <td>{item.unit_name}</td>
                  <td>{item.vehicle_type}</td>
                  <td>{item.purpose}</td>
                  <td>{item.operator_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
