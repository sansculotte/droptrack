import * as React from 'react'
import { useState } from 'react'
import { useInterval } from 'hooks/useInterval'


const randomByte = () => Math.round(Math.random() * 255).toString(16)

export default () => {

  const [ color, setColor ] = useState('#000')

  const ping = () => {
//    setColor(`#${randomByte()}${randomByte()}${randomByte()}`)
    setColor('#ac0000')
    setTimeout(() => setColor('#000000'), 200)
  }

  useInterval(ping, 1000)

  return (
    <div style={
      {
        width: '27px',
        height: '27px',
        borderRadius: '50%',
        backgroundColor: color,
        transition: 'background-color 50ms ease-in, 300ms ease-out',
        float: 'right',
      }
    } />
  )
}
