import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { Chart } from './components/chart'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/charts',
    element: <Chart />

  }
])  

export function App() {
  return <RouterProvider router={router} />
}

