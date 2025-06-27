"use client"

import { Input } from "./ui/input"
import ResumeUploader from "./ResumeUploader"
import JobContainer from "./ui/jobContainer"
import { useJobSearch } from "../jobSearchContext"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select"

export default function ClientHomePage() {

    const {updateParams} = useJobSearch()
    
    return (
    <main className="flex flex-col w-full min-h-screen bg-base-100 text-base-content px-6">
        {/* Everything stacked, now taking full width */}
        <div className="w-full flex flex-col gap-6">

        {/* Resume uploader centered but full width section */}
        <section className="p-8 w-full flex justify-center">
            <div className="w-full max-w-md">
            <ResumeUploader />
            </div>
        </section>

        {/* Inputs: full width, stacked on small screens */}
        <div className="flex flex-col md:flex-row gap-4 bg-base-200 p-6 rounded-lg shadow-md w-full max-w-7xl px-6">
            <Input 
                type="text" 
                placeholder="Job Title" 
                className="flex-1" 
                onChange={(e) => updateParams({what: e.target.value})}
            />
            <Input 
                type="text" 
                placeholder="Location" 
                className="flex-1" 
                onChange={(e) => updateParams({where: e.target.value})}
            />
            <Input 
                type="text" 
                placeholder="Max Distance" 
                className="w-full md:w-40" 
                onChange={(e) => {
                    const value = parseInt(e.target.value, 10)
                    updateParams({distance: isNaN(value) ? undefined : value})
                }}
            />
            <Select 
              onValueChange={(value)=> {
                updateParams({country: value})
              }}
            >
              <SelectTrigger>
                <SelectValue placeholder="Country" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="gb">United Kingdom</SelectItem>
                <SelectItem value="us">United States</SelectItem>
                <SelectItem value="at">Austria</SelectItem>
                <SelectItem value="au">Australia</SelectItem>
                <SelectItem value="be">Belgium</SelectItem>
                <SelectItem value="br">Brazil</SelectItem>
                <SelectItem value="ca">Canada</SelectItem>
                <SelectItem value="ch">Switzerland</SelectItem>
                <SelectItem value="de">Germany</SelectItem>
                <SelectItem value="es">Spain</SelectItem>
                <SelectItem value="fr">France</SelectItem>
                <SelectItem value="in">India</SelectItem>
                <SelectItem value="it">Italy</SelectItem>
                <SelectItem value="mx">Mexico</SelectItem>
                <SelectItem value="nl">Netherlands</SelectItem>
                <SelectItem value="nz">New Zealand</SelectItem>
                <SelectItem value="pl">Poland</SelectItem>
                <SelectItem value="sg">Singapore</SelectItem>
                <SelectItem value="za">South Africa</SelectItem>
              </SelectContent>
            </Select>
        </div>

        {/* Job container: make sure it matches the width */}
        <div className="w-full max-w-7xl px-6">
            <JobContainer />
        </div>
        </div>
    </main>
    )
}