import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      connectionId: null,
      isAuthenticated: false,
      login: (token, connectionId) => {
        set({ token, connectionId, isAuthenticated: true })
      },
      logout: () => {
        set({ token: null, connectionId: null, isAuthenticated: false })
      }
    }),
    {
      name: 'sf-bot-auth'
    }
  )
)
