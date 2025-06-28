"use client"

import { createContext, useContext, useState, ReactNode } from "react"

export type JobSearchParams = {
  country?: string
  what?: string
  where?: string
  distance?: number
  max_days_old?: number
  sort_by?: string
  sort_dir?: string
  salary_min?: number
  salary_max?: number
  salary_include_unknown?: string //set to "1" if you wanted
  full_time?: string //set to "1" if wanted for job type
  part_time?: string
  contract?: string
  permanent?: string
  company?: string
}

type JobSearchContextType = {
  params: JobSearchParams
  updateParams: (updates: Partial<JobSearchParams>) => void
}

const JobSearchContext = createContext<JobSearchContextType | null>(null)

export const useJobSearch = () => {
  const ctx = useContext(JobSearchContext)
  if (!ctx) throw new Error("useJobSearch must be used within JobSearchProvider")
  return ctx
}

export const JobSearchProvider = ({ children }: { children: ReactNode }) => {
  const [params, setParams] = useState<JobSearchParams>({})

  const updateParams = (updates: Partial<JobSearchParams>) => {
    setParams(prev => ({ ...prev, ...updates }))
  }

  return (
    <JobSearchContext.Provider value={{ params, updateParams }}>
      {children}
    </JobSearchContext.Provider>
  )
}
