"use client"

import React from "react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenuButton,
} from "./ui/sidebar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"
import SalaryRangeSlider from "./ui/salaryRangeSlider"
import { Input } from "./ui/input"
import { signOut } from "@/lib/actions"
import { useState, useTransition } from "react"
import { updateParameters } from "../serverActions/preferences"
import { useJobSearch } from "../jobSearchContext"

export default function AppSidebar() {
  const [sortBy, setSortBy] = useState("relevance")
  const [employmentType, setEmploymentType] = useState("")
  const [maxDaysOld, setMaxDaysOld] = useState("")
  const [salaryRange, setSalaryRange] = useState<[number, number]>([0, 200000])
  const [company, setCompany] = useState("")
  const {updateParams} = useJobSearch()

  const [isPending, startTransition] = useTransition()

  const handleSavePreferences = () => {
    startTransition(async () => {
      const result = await updateParameters({
        sortBy,
        employmentType,
        maxDaysOld,
        salaryRange,
        company,
      })

      if (result?.success) {
        // toast.success("Preferences saved successfully!")
        console.log("Preferences saved:", result.data)
      } else {
        // toast.error("Failed to save preferences")
        console.error(result?.error)
      }
    })
  }

  return (
    <Sidebar side="left" variant="sidebar" collapsible="none">
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Filters</SidebarGroupLabel>

          {/* Max Days Old Filter */}
          <SidebarGroupLabel>Max Days Old</SidebarGroupLabel>
          <SidebarGroupContent>
            <Select 
              value={maxDaysOld}
              onValueChange={(value)=> {
                setMaxDaysOld(value)
                updateParams({ max_days_old: parseInt(value, 10)})
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Any time" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="1">Last 24 hours</SelectItem>
                <SelectItem value="3">Last 3 days</SelectItem>
                <SelectItem value="7">Last 7 days</SelectItem>
                <SelectItem value="30">Last 30 days</SelectItem>
              </SelectContent>
            </Select>
          </SidebarGroupContent>

          {/* Sort By Filter */}
          <SidebarGroupLabel>Sort By</SidebarGroupLabel>
          <SidebarGroupContent>
            <Select 
              value={sortBy}
              onValueChange={(value)=> {
                setSortBy(value)
                updateParams({sort_by: value})
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Relevance" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="relevance">Relevance</SelectItem>
                <SelectItem value="date_posted">Date Posted</SelectItem>
                <SelectItem value="salary">Salary</SelectItem>
              </SelectContent>
            </Select>
          </SidebarGroupContent>

          {/* Salary Range Slider */}
          <SidebarGroupLabel>Salary Range</SidebarGroupLabel>
          <SidebarGroupContent>
            <SalaryRangeSlider 
              range={salaryRange} 
              setRange={(range: [number, number]) => {
                setSalaryRange(range)
                updateParams({salary_min: range[0], salary_max: range[1]})
              }}
            />
          </SidebarGroupContent>

          {/* Employment Type */}
          <SidebarGroupLabel>Employment Type</SidebarGroupLabel>
          <SidebarGroupContent>
            <Select 
              value={employmentType}
              onValueChange={(value) => {
                setEmploymentType(value)
                const employmentParams: Record<string, any> = {
                  "full-time": { full_time: "1", part_time: null, contract: null, permanent: null },
                  "part-time": { full_time: null, part_time: "1", contract: null, permanent: null },
                  "contract":  { full_time: null, part_time: null, contract: "1", permanent: null },
                  "permanent": { full_time: null, part_time: null, contract: null, permanent: "1" },
                }
                updateParams(employmentParams[value])
              }}
              >
              <SelectTrigger>
                <SelectValue placeholder="Any" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="full-time">Full-time</SelectItem>
                <SelectItem value="part-time">Part-time</SelectItem>
                <SelectItem value="contract">Contract</SelectItem>
                <SelectItem value="permanent">Permanent</SelectItem>
              </SelectContent>
            </Select>
          </SidebarGroupContent>

          {/* Company Filter */}
          {/* Will be an input */}
          <SidebarGroupLabel>Company</SidebarGroupLabel>
          <SidebarGroupContent>
            <Input 
              type="text" 
              placeholder="Search company..."
              value={company}
              onChange={(e)=> {
                setCompany(e.target.value)
                updateParams({company: e.target.value})
              }}
            />
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarMenuButton onClick={handleSavePreferences} disabled={isPending}>
          {isPending ? <span>Saving...</span> : <span>Save Preferences</span>}
        </SidebarMenuButton>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenuButton onClick={signOut}>
          <span>Log Out</span>
        </SidebarMenuButton>
      </SidebarFooter>
    </Sidebar>
  )
}
