import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useDropzone } from 'react-dropzone'
import apiClient from '../api/client'
import { Upload, FileText, X } from 'lucide-react'
import { Link } from 'react-router-dom'

function Workbooks() {
  const [uploading, setUploading] = useState(false)
  const queryClient = useQueryClient()

  const { data: workbooks, isLoading } = useQuery({
    queryKey: ['workbooks'],
    queryFn: async () => {
      const response = await apiClient.get('/workbooks')
      return response.data
    }
  })

  const uploadMutation = useMutation({
    mutationFn: async (file) => {
      const formData = new FormData()
      formData.append('file', file)
      const response = await apiClient.post('/workbooks/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['workbooks'])
      setUploading(false)
    },
    onError: () => {
      setUploading(false)
    }
  })

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setUploading(true)
        uploadMutation.mutate(acceptedFiles[0])
      }
    },
    multiple: false
  })

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Workbooks</h1>
        <p className="text-gray-600 mt-2">Upload and manage your configuration workbooks</p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
          isDragActive
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
        } ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} disabled={uploading} />
        <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        {uploading ? (
          <p className="text-gray-600">Uploading...</p>
        ) : isDragActive ? (
          <p className="text-indigo-600 font-medium">Drop the file here</p>
        ) : (
          <>
            <p className="text-gray-700 font-medium mb-2">
              Drag & drop a workbook file here, or click to select
            </p>
            <p className="text-gray-500 text-sm">
              Supports Excel (.xlsx, .xls) and CSV files
            </p>
          </>
        )}
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Your Workbooks</h2>
        {isLoading ? (
          <p className="text-gray-600">Loading...</p>
        ) : workbooks && workbooks.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {workbooks.map((workbook) => (
              <Link
                key={workbook.id}
                to={`/workbooks/${workbook.id}`}
                className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition border border-gray-200"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <FileText className="w-8 h-8 text-indigo-600" />
                    <div>
                      <h3 className="font-semibold text-gray-900">{workbook.name}</h3>
                      <p className="text-sm text-gray-500 mt-1">
                        Created: {new Date(workbook.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
                {workbook.description && (
                  <p className="text-sm text-gray-600 mt-3">{workbook.description}</p>
                )}
              </Link>
            ))}
          </div>
        ) : (
          <div className="bg-white p-12 rounded-lg shadow text-center">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No workbooks uploaded yet</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Workbooks
