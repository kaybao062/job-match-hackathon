"use client";

import { ReactNode } from 'react'
import { SidebarProvider } from '@/app/components/ui/sidebar'
import { JobSearchProvider } from '../jobSearchContext';
import AppSidebar from '../components/app-sidebar'

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <JobSearchProvider>
      <div className="grid grid-cols-[250px_1fr]">
        {/* Sidebar is wrapped with SidebarProvider */}
        <SidebarProvider>
          <div>
            <AppSidebar />
          </div>
        </SidebarProvider>

        {/* Main content goes outside the SidebarProvider */}
        <main className="p-8 flex flex-col items-center w-full">
          <div className='w-full max-w-7xl px-6'>
            {children}
          </div>
        </main>
      </div>
    </JobSearchProvider>
  )
} 