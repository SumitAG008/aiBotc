import { useParams } from 'react-router-dom'
import { useQuery, useMutation } from '@tanstack/react-query'
import apiClient from '../api/client'
import { Play, FileText, History, Brain, AlertCircle } from 'lucide-react'
import { useState } from 'react'

function WorkbookDetail() {
  const { id } = useParams()
  const [selectedVersion, setSelectedVersion] = useState(null)

  const { data: workbook, isLoading } = useQuery({
    queryKey: ['workbook', id],
    queryFn: async () => {
      const response = await apiClient.get(`/workbooks/${id}`)
      return response.data
    },
    enabled: !!id
  })

  const { data: versions } = useQuery({
    queryKey: ['workbook-versions', id],
    queryFn: async () => {
      const response = await apiClient.get(`/workbooks/${id}/versions`)
      return response.data
    },
    enabled: !!id
  })

  const analyzeMutation = useMutation({
    mutationFn: async () => {
      const response = await apiClient.post(`/workbooks/${id}/analyze`)
      return response.data
    }
  })

  const implementMutation = useMutation({
    mutationFn: async (versionId) => {
      const response = await apiClient.post(`/workbooks/${id}/implement`, {
        version_id: versionId
      })
      return response.data
    }
  })

  if (isLoading) {
    return <div className="p-6">Loading...</div>
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">{workbook?.name}</h1>
        <p className="text-gray-600 mt-2">{workbook?.description || 'No description'}</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <Brain className="w-5 h-5" />
                AI Analysis
              </h2>
              <button
                onClick={() => analyzeMutation.mutate()}
                disabled={analyzeMutation.isPending}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50"
              >
                {analyzeMutation.isPending ? 'Analyzing...' : 'Analyze Workbook'}
              </button>
            </div>

            {analyzeMutation.data && (
              <div className="space-y-4">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-semibold text-blue-900 mb-2">Analysis Results</h3>
                  <p className="text-sm text-blue-800">
                    Estimated Changes: {analyzeMutation.data.estimated_changes}
                  </p>
                  <p className="text-sm text-blue-800">
                    Complexity: {analyzeMutation.data.complexity}
                  </p>
                  <p className="text-sm text-blue-800">
                    Risk Level: {analyzeMutation.data.risk_level}
                  </p>
                </div>

                {analyzeMutation.data.recommendations && (
                  <div>
                    <h4 className="font-semibold mb-2">Recommendations:</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                      {analyzeMutation.data.recommendations.map((rec, idx) => (
                        <li key={idx}>{rec.message}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {analyzeMutation.isError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800">Error analyzing workbook</p>
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <History className="w-5 h-5" />
              Version History
            </h2>
            {versions && versions.length > 0 ? (
              <div className="space-y-3">
                {versions.map((version) => (
                  <div
                    key={version.id}
                    className={`border rounded-lg p-4 ${
                      selectedVersion === version.id
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-semibold">Version {version.version_number}</p>
                        <p className="text-sm text-gray-600">
                          {new Date(version.created_at).toLocaleString()}
                        </p>
                        {version.changes_summary && (
                          <p className="text-sm text-gray-700 mt-1">
                            {version.changes_summary}
                          </p>
                        )}
                      </div>
                      <button
                        onClick={() => setSelectedVersion(version.id)}
                        className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
                      >
                        Select
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-600">No versions available</p>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Actions</h2>
            <div className="space-y-3">
              <button
                onClick={() => {
                  if (selectedVersion || (versions && versions.length > 0)) {
                    implementMutation.mutate(selectedVersion || versions[0].id)
                  }
                }}
                disabled={implementMutation.isPending || !versions || versions.length === 0}
                className="w-full bg-green-600 text-white px-4 py-3 rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                <Play className="w-5 h-5" />
                {implementMutation.isPending ? 'Implementing...' : 'Implement Configuration'}
              </button>
            </div>

            {implementMutation.data && (
              <div className="mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-green-800 font-semibold">Implementation Successful!</p>
                <p className="text-sm text-green-700 mt-1">
                  Changes Applied: {implementMutation.data.changes_applied}
                </p>
              </div>
            )}

            {implementMutation.isError && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800">Implementation failed</p>
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <AlertCircle className="w-5 h-5" />
              Important Notes
            </h2>
            <ul className="space-y-2 text-sm text-gray-700">
              <li>• Review AI analysis before implementing</li>
              <li>• Ensure you have proper permissions in SuccessFactors</li>
              <li>• Changes are applied immediately to your SF instance</li>
              <li>• Keep backups of your configurations</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default WorkbookDetail
