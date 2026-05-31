import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      setLoading(false)
      return
    }
    api.get('/auth/me').then((res) => setUser(res.data)).catch(() => localStorage.removeItem('token')).finally(() => setLoading(false))
  }, [])

  const value = useMemo(() => ({
    user,
    loading,
    async login(username, password) {
      const res = await api.post('/auth/login', { username, password })
      localStorage.setItem('token', res.data.access_token)
      const me = await api.get('/auth/me')
      setUser(me.data)
    },
    logout() {
      localStorage.removeItem('token')
      setUser(null)
    }
  }), [user, loading])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
