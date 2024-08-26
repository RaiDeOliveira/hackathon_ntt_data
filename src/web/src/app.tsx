import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { Temperature } from './pages/temperature'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/temperature',
    element: <Temperature />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

