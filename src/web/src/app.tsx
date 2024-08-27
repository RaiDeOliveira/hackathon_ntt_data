import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import Video from './pages/video'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/video',
    element: <Video />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

