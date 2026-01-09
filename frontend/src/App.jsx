import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Workbooks from './pages/Workbooks'
import WorkbookDetail from './pages/WorkbookDetail'
import { useAuthStore } from './store/authStore'
import Layout from './components/Layout'

const queryClient = new QueryClient()

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuthStore()
  return isAuthenticated ? children : <Navigate to="/login" />
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <Layout>
                  <Dashboard />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/workbooks"
            element={
              <PrivateRoute>
                <Layout>
                  <Workbooks />
                </Layout>
              </PrivateRoute>
            }
          />
          <Route
            path="/workbooks/:id"
            element={
              <PrivateRoute>
                <Layout>
                  <WorkbookDetail />
                </Layout>
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </QueryClientProvider>
  )
}

export default App
