import { AlertTriangle, RadioTower, ShieldCheck, Truck } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { api } from '../api/client'

const cardMeta = [
  ['vehicles_today', 'Vehicles Today', Truck],
  ['active_inside', 'Active Inside', RadioTower],
  ['total_registered', 'Registered Fleet', ShieldCheck],
  ['suspicious_entries', 'Suspicious Entries', AlertTriangle]
]

export default function Dashboard() {
  const [data, setData] = useState(null)
  useEffect(() => {
    api.get('/dashboard/summary').then((res) => setData(res.data))
  }, [])

  if (!data) return <div className="py-10 text-moss">Loading dashboard...</div>

  return (
    <div className="space-y-6">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-moss">Operational Overview</p>
          <h1 className="mt-2 text-3xl font-black">Army Vehicle Movement Dashboard</h1>
        </div>
        <div className="rounded-lg border border-moss/25 bg-bunker/70 px-4 py-3 text-sm text-white/70">Live readiness: active</div>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cardMeta.map(([key, label, Icon]) => (
          <div key={key} className="glass rounded-lg p-5 shadow-tactical">
            <div className="flex items-center justify-between">
              <p className="text-sm text-white/60">{label}</p>
              <Icon className="text-moss" size={22} />
            </div>
            <p className="mt-4 text-4xl font-black">{data.stats[key]}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <div className="glass rounded-lg p-5">
          <h2 className="mb-4 text-lg font-bold">Daily Movement</h2>
          <div className="h-80">
            <ResponsiveContainer>
              <AreaChart data={data.daily_movement}>
                <defs>
                  <linearGradient id="entries" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#8b9b4f" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#8b9b4f" stopOpacity={0.05} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="date" stroke="#9aa58d" />
                <YAxis stroke="#9aa58d" />
                <Tooltip contentStyle={{ background: '#10160f', border: '1px solid rgba(139,155,79,.3)' }} />
                <Area type="monotone" dataKey="entries" stroke="#8b9b4f" fill="url(#entries)" />
                <Area type="monotone" dataKey="exits" stroke="#f2c94c" fill="transparent" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="glass rounded-lg p-5">
          <h2 className="mb-4 text-lg font-bold">Recent Activity</h2>
          <div className="space-y-3">
            {data.recent_activity.map((item) => (
              <div key={item.id} className="rounded-lg border border-white/10 bg-white/[0.03] p-3">
                <div className="flex justify-between gap-3">
                  <p className="font-bold">{item.vehicle_number}</p>
                  <span className="text-xs font-bold text-moss">{item.movement_type}</span>
                </div>
                <p className="mt-1 text-sm text-white/55">{item.camera} by {item.operator}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
