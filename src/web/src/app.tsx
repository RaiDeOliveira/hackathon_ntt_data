import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { VideoFeed } from './pages/video'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/video',
    element: <VideoFeed />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

