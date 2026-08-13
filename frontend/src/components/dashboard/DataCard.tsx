import React from 'react'

interface Props {
    data: number
    label: string
}

function DataCard({data, label}:Props) {
  return (
    <div className='p-4 bg-blue-500 text-xl text-white font-semibold rounded-sm'>
      {data} {label}
    </div>
  )
}

export default DataCard
