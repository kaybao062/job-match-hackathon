"use client"

import * as Slider from "@radix-ui/react-slider"
import {useState} from "react"

type SalaryRangeSliderProps = {
    range: [number, number]
    setRange: (range: [number, number]) => void
}

export default function SalaryRangeSlider({range, setRange}: SalaryRangeSliderProps) {
    return (
        <div className="w-full max-w-md">
            {/* <label className="block mb-2 text-sm font-medium">Salary Range</label> */}
            <Slider.Root
                className="relative flex items-center select-none touch-none w-full h-5"
                value={range}
                onValueChange={(val) => setRange(val as [number, number])}
                min={0}
                max={200000}
                step={1000}
            >
                <Slider.Track className="bg-gray-200 relative grow rounded-full h-[3px]">
                    <Slider.Range className="absolute bg-blue-500 rounded-full h-full"/>
                </Slider.Track>
                <Slider.Thumb className="block w-4 h-4 bg-blue-500 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"/>
                <Slider.Thumb className="block w-4 h-4 bg-blue-500 rounded-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400"/>
            </Slider.Root>
            <div className="mt-2 text-sm text-gray-700">
                ${range[0].toLocaleString()} - ${range[1].toLocaleString()}
            </div>
        </div>
    )
}