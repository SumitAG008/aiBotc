import { useQuery } from '@tanstack/react-query'
import apiClient from '../api/client'
import { FileText, Upload, CheckCircle, AlertCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

function Dashboard() {
  const { data: workbooks, isLoading } = useQuery({
    queryKey: ['workbooks'],
    queryFn: async () => {
      const response = await apiClient.get('/workbooks')
      return response.data
    }
  })

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Manage your SuccessFactors configurations</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Total Workbooks</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {workbooks?.length || 0}
              </p>
            </div>
            <FileText className="w-12 h-12 text-indigo-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Ready to Implement</p>
              <p className="text-3xl font-bold text-green-600 mt-2">0</p>
            </div>
            <CheckCircle className="w-12 h-12 text-green-600" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm">Pending Review</p>
              <p className="text-3xl font-bold text-yellow-600 mt-2">0</p>
            </div>
            <AlertCircle className="w-12 h-12 text-yellow-600" />
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold">Recent Workbooks</h2>
            <Link
              to="/workbooks"
              className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Upload Workbook
            </Link>
          </div>
        </div>

        <div className="p-6">
          {isLoading ? (
            <p className="text-gray-600">Loading...</p>
          ) : workbooks && workbooks.length > 0 ? (
            <div className="space-y-4">
              {workbooks.map((workbook) => (
                <Link
                  key={workbook.id}
                  to={`/workbooks/${workbook.id}`}
                  className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-900">{workbook.name}</h3>
                      <p className="text-sm text-gray-600 mt-1">
                        {workbook.description || 'No description'}
                      </p>
                    </div>
                    <FileText className="w-6 h-6 text-gray-400" />
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600 mb-4">No workbooks yet</p>
              <Link
                to="/workbooks"
                className="inline-block bg-indigo-600 text-white px-6 py-2 rounded-md hover:bg-indigo-700"
              >
                Upload Your First Workbook
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard
