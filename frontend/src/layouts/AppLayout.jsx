import { LayoutDashboard, LogOut, Logs, Menu, Scan, ShieldCheck, UserPlus, X } from 'lucide-react'
import { useState } from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function AppLayout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)

  const links = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/camera', label: 'Detection', icon: Scan },
    { to: '/vehicles', label: 'Registry', icon: ShieldCheck },
    { to: '/logs', label: 'Movement Logs', icon: Logs },
    { to: '/register', label: 'Registration', icon: UserPlus },
  ]

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex min-h-screen bg-[#080b08] text-white">
      {/* Sidebar Desktop */}
      <aside className="hidden w-72 flex-col border-r border-moss/20 bg-[#080b08]/90 backdrop-blur-xl lg:flex fixed inset-y-0">
        <div className="flex h-20 items-center gap-3 px-8 border-b border-white/5">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-moss text-[#080b08] shadow-lg shadow-moss/20">
            <ShieldCheck size={24} />
          </div>
          <span className="text-xl font-black tracking-tighter text-white">
            ARMOR<span className="text-moss">SCAN</span>
          </span>
        </div>

        <nav className="flex-1 space-y-1 p-6">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 font-bold transition-all ${
                  isActive 
                    ? 'bg-moss/10 text-moss border border-moss/20' 
                    : 'text-white/40 hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <link.icon size={20} />
              <span className="text-xs uppercase tracking-widest">{link.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="border-t border-white/5 p-6">
          <div className="flex items-center gap-3 rounded-2xl bg-white/5 p-4 border border-white/5">
            <div className="h-10 w-10 rounded-full bg-moss/20 flex items-center justify-center text-moss font-black">
              {user?.username?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1 overflow-hidden">
              <p className="truncate text-sm font-black text-white">{user?.username || 'Operator'}</p>
              <p className="text-[10px] font-bold text-white/30 uppercase tracking-widest">Active Duty</p>
            </div>
            <button 
              onClick={handleLogout}
              className="rounded-lg p-2 text-white/40 hover:bg-red-500/10 hover:text-red-400 transition-colors"
              title="Logout"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </aside>

      {/* Mobile Nav */}
      <div className="flex flex-1 flex-col lg:pl-72">
        <header className="flex h-16 items-center justify-between border-b border-moss/20 bg-[#080b08]/90 px-6 backdrop-blur-xl lg:hidden sticky top-0 z-20">
          <Link to="/" className="flex items-center gap-2">
            <ShieldCheck className="text-moss" size={24} />
            <span className="font-black tracking-tighter text-white uppercase">ArmorScan</span>
          </Link>
          <button onClick={() => setMobileOpen(!mobileOpen)} className="text-white">
            {mobileOpen ? <X /> : <Menu />}
          </button>
        </header>

        {mobileOpen && (
          <div className="fixed inset-0 z-50 bg-[#080b08]/95 p-6 lg:hidden">
            <div className="mb-8 flex items-center justify-between">
              <span className="font-black text-white uppercase tracking-tighter">Navigation</span>
              <button onClick={() => setMobileOpen(false)}><X /></button>
            </div>
            <nav className="space-y-4">
              {links.map((link) => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  onClick={() => setMobileOpen(false)}
                  className={({ isActive }) =>
                    `flex items-center gap-4 rounded-xl p-4 font-black ${
                      isActive ? 'bg-moss text-black' : 'text-white/60'
                    }`
                  }
                >
                  <link.icon size={24} />
                  <span className="text-lg uppercase tracking-widest">{link.label}</span>
                </NavLink>
              ))}
              <button 
                onClick={handleLogout}
                className="flex w-full items-center gap-4 rounded-xl p-4 font-black text-red-400 hover:bg-red-400/10"
              >
                <LogOut size={24} />
                <span className="text-lg uppercase tracking-widest">Sign Out</span>
              </button>
            </nav>
          </div>
        )}

        <main className="flex-1 p-6 lg:p-10">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
