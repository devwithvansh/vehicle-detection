import { Download, FileDown, Filter } from 'lucide-react'
import { useEffect, useState } from 'react'
import { api } from '../api/client'

export default function LogsPage() {
  const [logs, setLogs] = useState([])
  const [movementType, setMovementType] = useState('')

  useEffect(() => {
    api.get('/logs', { params: movementType ? { movement_type: movementType } : {} }).then((res) => setLogs(res.data))
  }, [movementType])

  async function downloadExport(path, filename) {
    const res = await api.get(path, { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-moss">Audit Trail</p>
          <h1 className="mt-2 text-3xl font-black">Vehicle Logs</h1>
        </div>
        <div className="flex gap-3">
          <button className="btn btn-secondary" onClick={() => downloadExport('/logs/export.pdf', 'vehicle_logs.pdf')}><FileDown size={18} /> Export PDF</button>
          <button className="btn btn-primary" onClick={() => downloadExport('/logs/export.csv', 'vehicle_logs.csv')}><Download size={18} /> Export CSV</button>
        </div>
      </header>
      <div className="glass rounded-lg p-4">
        <label className="mb-4 flex max-w-xs items-center gap-2">
          <Filter size={18} className="text-moss" />
          <select className="input" value={movementType} onChange={(e) => setMovementType(e.target.value)}>
            <option value="">All movements</option>
            <option value="ENTRY">Entry</option>
            <option value="EXIT">Exit</option>
          </select>
        </label>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[900px] text-left text-sm">
            <thead className="text-white/50">
              <tr><th className="p-3">Vehicle</th><th>Movement</th><th>Entry</th><th>Exit</th><th>Camera</th><th>Operator</th><th>Confidence</th></tr>
            </thead>
            <tbody>
              {logs.map((item) => (
                <tr key={item.id} className="border-t border-white/10">
                  <td className="p-3 font-bold text-moss">{item.vehicle_number}</td>
                  <td>{item.movement_type}</td>
                  <td>{item.entry_time ? new Date(item.entry_time).toLocaleString() : '-'}</td>
                  <td>{item.exit_time ? new Date(item.exit_time).toLocaleString() : '-'}</td>
                  <td>{item.camera_name || '-'}</td>
                  <td>{item.operator_name || '-'}</td>
                  <td>{item.confidence_score ? `${Math.round(item.confidence_score * 100)}%` : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
