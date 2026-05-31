import { useEffect, useState } from 'react'

export default function ToastHost() {
  const [items, setItems] = useState([])
  useEffect(() => {
    const handler = (event) => {
      const id = crypto.randomUUID()
      setItems((current) => [...current, { id, message: event.detail }])
      setTimeout(() => setItems((current) => current.filter((item) => item.id !== id)), 3600)
    }
    window.addEventListener('toast', handler)
    return () => window.removeEventListener('toast', handler)
  }, [])
  return (
    <div className="fixed right-4 top-4 z-50 space-y-3">
      {items.map((item) => (
        <div key={item.id} className="glass rounded-lg px-4 py-3 text-sm text-white shadow-tactical">
          {item.message}
        </div>
      ))}
    </div>
  )
}
