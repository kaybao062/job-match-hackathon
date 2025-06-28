"use client"

import { useState } from "react"
import {createClient} from "@/lib/supabase/client"


export default function ResumeUploader() {
  const [fileName, setFileName] = useState("")
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState("")

  const supabase = createClient()

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setFileName(file.name)
    setUploading(true)
    setMessage("")

    const user = await supabase.auth.getUser()
    const userId = user.data.user?.id

    if (!userId) {
      setMessage("You must be logged in to upload a file.")
      setUploading(false)
      return
    }
    const filePath = `${userId}/${file.name}`

    const {error} = await supabase.storage
      .from("user-resume")
      .upload(filePath, file, {
        cacheControl: "3600",
        upsert: true,
      })

      if (error) {
        console.error("Upload error: ", error)
        setMessage("Failed to upload resume.")
      } else {
        setMessage("Resume upload successfully!")
      }

      setUploading(false)
  }

  return (
    <label className="h-35 w-[500px] border-dashed border-2 border-primary flex flex-col items-center justify-center cursor-pointer bg-base-100 hover:bg-base-200 transition rounded-lg p-4 text-center w-full">
      <input type="file" accept=".pdf,.doc,.docx" onChange={handleFileChange} className="hidden" />
      <p className="text-lg font-semibold mb-2">Click or drag resume here</p>
      <p className="text-sm text-base-content/60">PDF or DOCX, max 5MB</p>
      {fileName && <p className="mt-4 text-success">{fileName}</p>}
      {uploading && <p className="text-info mt-2">Uploading...</p>}
      {message && <p className="mt-2 text-sm text-base-content">{message}</p>}
    </label>
  )
}