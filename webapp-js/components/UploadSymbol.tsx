import * as React from 'react'

interface Props {
  color?: string
}

const UploadSymbol = (props: Props) => {
  const color = props.color || '#cccccc'
  return (
    <svg width="auto" height="100%" viewBox="0 15 100 100" style={{fill: color}}>
      <path d="m 24.946428,67.190471 h 5.008186 V 78.340769 H 69.925593 V 67.190471 H 74.93378 V 82.68749 H 24.946428 Z" /> 
      <path d="M 49.98735,39.598211 39.970979,50.276029 h 6.992562 v 22.206109 h 6.047618 V 50.276029 h 6.992559 z" />
    </svg>
  )
}

export default UploadSymbol
