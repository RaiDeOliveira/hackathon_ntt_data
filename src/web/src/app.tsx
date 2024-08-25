import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { Chat } from './pages/chat'
import { Video } from './pages/video'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/chat',
    element: <Chat />
  },
  {
    path: '/video',
    element: <Video />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

