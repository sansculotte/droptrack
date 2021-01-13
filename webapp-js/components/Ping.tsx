import * as React from 'react'
import { useEffect, useState } from 'react'


export default (props: {timeStamp: number}) => {

  const [ color, setColor ] = useState('#000')

  const ping = () => {
    setColor('#ac0000')
    setTimeout(() => setColor('#000000'), 200)
  }

  useEffect(ping, [props.timeStamp])

  return (
    <div style={
      {
        width: '50px',
        height: '50px',
        borderRadius: '50%',
        backgroundColor: color,
        transition: 'background-color 50ms ease-in, 300ms ease-out',
        float: 'right',
      }
    } />
  )
}
