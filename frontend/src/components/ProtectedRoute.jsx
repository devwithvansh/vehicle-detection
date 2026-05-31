import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="min-h-screen bg-bunker p-8 text-moss">Loading command console...</div>
  if (!user) return <Navigate to="/login" replace />
  return children
}
