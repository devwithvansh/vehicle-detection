import { AlertTriangle, Activity, Clock, Truck, TrendingUp } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { api } from '../api/client'

const cardMeta = [
  ['vehicles_today', 'Vehicles Today', Truck, 'bg-blue-500/10 text-blue-400'],
  ['active_inside', 'Currently Inside', Activity, 'bg-green-500/10 text-green-400'],
  ['total_registered', 'Total Fleet', TrendingUp, 'bg-moss/10 text-moss'],
  ['suspicious_entries', 'Flagged Entries', AlertTriangle, 'bg-red-500/10 text-red-400']
]

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/dashboard/summary')
      .then((res) => {
        setData(res.data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="space-y-6">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-moss font-bold">Operational Overview</p>
          <h1 className="mt-2 text-3xl font-black text-white">Army Vehicle Movement Dashboard</h1>
        </header>
        <div className="flex items-center justify-center py-20">
          <div className="text-center">
            <div className="w-12 h-12 border-4 border-moss border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-moss font-bold tracking-widest">LOADING SYSTEM...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="space-y-6">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-moss font-bold">Operational Overview</p>
          <h1 className="mt-2 text-3xl font-black text-white">Army Vehicle Movement Dashboard</h1>
        </header>
        <div className="flex items-center justify-center py-20 bg-white/5 border border-white/10 rounded-xl">
          <p className="text-white/40 font-bold">Unable to load dashboard data</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-moss font-bold">Operational Overview</p>
          <h1 className="mt-2 text-3xl font-black text-white">Army Vehicle Movement Dashboard</h1>
        </div>
        <div className="flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-lg">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
          <span className="text-xs font-bold text-white/60 uppercase tracking-widest">Live System Active</span>
        </div>
      </header>

      {/* Stats Cards */}
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {cardMeta.map(([key, label, Icon, colors]) => (
          <div key={key} className={`bg-white/[0.03] border border-white/10 rounded-xl p-6 hover:border-white/20 transition-all group`}>
            <div className="flex items-center justify-between mb-4">
              <p className="text-xs font-bold text-white/40 uppercase tracking-widest">{label}</p>
              <div className={`p-2 rounded-lg ${colors}`}>
                <Icon size={20} />
              </div>
            </div>
            <p className="text-4xl font-black text-white">{data.stats[key]}</p>
          </div>
        ))}
      </section>

      {/* Charts & Activity */}
      <section className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        {/* Daily Movement Chart */}
        <div className="bg-white/[0.03] border border-white/10 rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-black text-white flex items-center gap-2">
              <TrendingUp className="text-moss" size={24} /> Daily Movement
            </h2>
            <span className="text-[10px] font-bold text-white/30 uppercase tracking-widest">Last 7 days</span>
          </div>
          <div className="h-80 -mx-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.daily_movement}>
                <defs>
                  <linearGradient id="entries" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#8b9b4f" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#8b9b4f" stopOpacity={0.05} />
                  </linearGradient>
                  <linearGradient id="exits" x1="0" x2="0" y1="0" y2="1">
                    <stop offset="5%" stopColor="#f2c94c" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#f2c94c" stopOpacity={0.05} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="date" stroke="#9aa58d" style={{ fontSize: '12px' }} />
                <YAxis stroke="#9aa58d" style={{ fontSize: '12px' }} />
                <Tooltip 
                  contentStyle={{ 
                    background: 'rgba(8,11,8,0.95)', 
                    border: '1px solid rgba(139,155,79,0.3)',
                    borderRadius: '8px'
                  }} 
                  labelStyle={{ color: '#8b9b4f' }}
                />
                <Area type="monotone" dataKey="entries" stroke="#8b9b4f" fill="url(#entries)" name="Entries" />
                <Area type="monotone" dataKey="exits" stroke="#f2c94c" fill="url(#exits)" name="Exits" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white/[0.03] border border-white/10 rounded-xl p-6 flex flex-col">
          <h2 className="text-lg font-black text-white flex items-center gap-2 mb-6">
            <Clock className="text-moss" size={24} /> Recent Activity
          </h2>
          <div className="space-y-3 flex-1 overflow-y-auto pr-2">
            {data.recent_activity && data.recent_activity.length > 0 ? (
              data.recent_activity.map((item) => (
                <div key={item.id} className="rounded-lg border border-white/5 bg-white/[0.02] p-4 hover:border-white/10 transition-all group">
                  <div className="flex justify-between items-start gap-3 mb-2">
                    <p className="font-black text-white text-lg tracking-tight">{item.vehicle_number}</p>
                    <span className={`text-[10px] font-black uppercase tracking-tighter px-2 py-1 rounded ${
                      item.movement_type === 'ENTRY' 
                        ? 'bg-green-500/20 text-green-400' 
                        : 'bg-red-500/20 text-red-400'
                    }`}>
                      {item.movement_type}
                    </span>
                  </div>
                  <p className="text-xs text-white/40 font-medium">
                    {item.camera} • {item.operator}
                  </p>
                  <p className="text-[10px] text-white/20 mt-1">
                    {new Date(item.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              ))
            ) : (
              <div className="flex items-center justify-center py-8 text-center opacity-30">
                <p className="text-sm text-white/40 font-medium">No recent activity</p>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}
