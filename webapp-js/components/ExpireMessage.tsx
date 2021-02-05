import * as React from 'react'
import { useEffect, useState } from 'react'

import * as style from './ExpireMessage.scss'


interface Props {
  delay?: number
  timeStamp: number
  children: React.ReactNode
}

export default (props: Props)  => {

  const delay = props.delay || 3000
  const [ visible, setVisible ] = useState(true)
  let id: number | undefined

  useEffect(() => setVisible(true), [props.timeStamp])

  useEffect(() => {
    const hide = () => setVisible(false)
    if (delay > 0) {
      id = setTimeout(hide, delay)
      return () => clearTimeout(id)
    }
  })

  return visible
    ? <div className={style.message}>{props.children}</div>
    : null
}
