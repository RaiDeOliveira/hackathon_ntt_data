import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Home } from './pages/home'
import { Chat } from './pages/chat'
import { Temperature } from './pages/temperature'

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
    path: '/temperature',
    element: <Temperature />
  }
])  

export function App() {
  return <RouterProvider router={router} />
}

