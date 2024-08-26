import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { ChatPage } from './pages/chatPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/chat',
    element: <ChatPage />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

