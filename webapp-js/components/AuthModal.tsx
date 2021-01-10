import * as React from 'react'
import { useState } from 'react'


interface Props {
  setKey: (key: string) => void
}


export default (props: Props) => {

  const [ key, setKey ] = useState('')

  const handleSubmit = (ev: any) => {
    ev.preventDefault()
    props.setKey(key)
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={key}
          placeholder="API Key"
          onChange={(ev: any) => setKey(ev.currentTarget.value)}
        /> 
      </form>
    </div>
  )
}
