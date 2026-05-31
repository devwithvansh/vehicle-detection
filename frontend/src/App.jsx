import { Navigate, Route, Routes } from 'react-router-dom'
import ToastHost from './components/ToastHost'
import ProtectedRoute from './components/ProtectedRoute'
import AppLayout from './layouts/AppLayout'
import CameraPage from './pages/CameraPage'
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'
import LogsPage from './pages/LogsPage'
import RegisterVehicle from './pages/RegisterVehicle'
import VehiclesPage from './pages/VehiclesPage'

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="/camera" element={<CameraPage />} />
          <Route path="/vehicles" element={<VehiclesPage />} />
          <Route path="/logs" element={<LogsPage />} />
          <Route path="/register" element={<RegisterVehicle />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <ToastHost />
    </>
  )
}
