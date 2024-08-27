import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { Temperature } from './pages/temperature'
import Video from './pages/video'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/temperature',
    element: <Temperature />
  },
  {
    path: '/video',
    element: <Video />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

