import { BarChart3, Camera, ClipboardList, LogOut, Shield, Truck, Users } from 'lucide-react'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const links = [
  ['/', BarChart3, 'Dashboard'],
  ['/camera', Camera, 'Detection'],
  ['/vehicles', Truck, 'Vehicles'],
  ['/logs', ClipboardList, 'Logs'],
  ['/register', Users, 'Register']
]

export default function AppLayout() {
  const { user, logout } = useAuth()
  return (
    <div className="min-h-screen text-white">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-72 border-r border-moss/20 bg-bunker/90 p-5 backdrop-blur lg:block">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-lg bg-moss text-bunker">
            <Shield size={24} />
          </div>
          <div>
            <p className="text-sm uppercase tracking-[0.25em] text-moss">Command</p>
            <h1 className="font-bold">Vehicle Sentinel</h1>
          </div>
        </div>
        <nav className="mt-10 space-y-2">
          {links.map(([to, Icon, label]) => (
            <NavLink key={to} to={to} className={({ isActive }) => `flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-semibold ${isActive ? 'bg-moss text-bunker' : 'text-white/70 hover:bg-white/5 hover:text-white'}`}>
              <Icon size={18} /> {label}
            </NavLink>
          ))}
        </nav>
        <div className="absolute bottom-5 left-5 right-5">
          <div className="glass rounded-lg p-4">
            <p className="font-semibold">{user?.full_name}</p>
            <p className="text-sm text-white/55">{user?.role}</p>
            <button className="btn btn-secondary mt-4 w-full" onClick={logout}><LogOut size={17} /> Logout</button>
          </div>
        </div>
      </aside>
      <header className="sticky top-0 z-20 border-b border-moss/20 bg-bunker/90 p-3 backdrop-blur lg:hidden">
        <div className="mb-3 flex items-center justify-between">
          <div className="flex items-center gap-2 font-black"><Shield size={20} className="text-moss" /> Vehicle Sentinel</div>
          <button className="rounded-lg border border-moss/25 p-2 text-white/70" onClick={logout} aria-label="Logout"><LogOut size={18} /></button>
        </div>
        <nav className="flex gap-2 overflow-x-auto pb-1">
          {links.map(([to, Icon, label]) => (
            <NavLink key={to} to={to} className={({ isActive }) => `flex shrink-0 items-center gap-2 rounded-lg px-3 py-2 text-xs font-semibold ${isActive ? 'bg-moss text-bunker' : 'bg-white/5 text-white/70'}`}>
              <Icon size={15} /> {label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="lg:pl-72">
        <div className="mx-auto max-w-7xl px-4 py-5 sm:px-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
