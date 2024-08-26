import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { Temperature } from './pages/temperature'
import { ChatPage } from './pages/chatPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/chat',
    element: <ChatPage />
  },
  {
    path: '/temperature',
    element: <Temperature />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

