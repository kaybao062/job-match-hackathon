'use client'

import * as React from 'react'
import { useState } from 'react'


export default function JobContainer() {
    const [jobTitle, setJobTitle] = useState("Frontend Developer")
    const [company, setCompany] = useState("Lorem Ipsum Inc.")
    const [score, setScore] = useState(87)
    const [educationRanking, setEducationRanking] = useState("Bachelor's degree in Computer Science from a top 20 university.")
    const [skillsRanking, setSkillsRanking] = useState("Proficient in React, Tailwind CSS, and TypeScript.")
    const [experienceRanking, setExperienceRanking] = useState("3 years of relevant industry experience.")

    // need to import function that retrieves the results from ai agent to be displayed for the fields
    
    return (
       <div className="bg-white rounded-2xl shadow-md my-4 p-6 w-full">
            <div>
                <span className='font-semibold'>Job Title: </span>
                <span>{jobTitle}</span>
            </div>
            <div>
               <span className='font-semibold'>Company: </span> 
               <span>{company}</span>
            </div>
            <div>
                <span className='font-semibold'>Score: </span>
                <span>{score}</span>
            </div>
            <div className='py-4'>
                <p className='font-semibold'>Reason of ranking - Education:</p>
                <p>{educationRanking}</p>
            </div>
            <div className='py-4'>
                <p className='font-semibold'>Reason of ranking - Skills:</p>
                <p>{skillsRanking}</p>
            </div>
            <div className='py-4'>
                <p className='font-semibold'>Reason of ranking - Experience:</p>
                <p>{experienceRanking}</p>
            </div>
        </div>
    )
}