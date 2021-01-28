import React from 'react'

import { AutoCover } from 'interfaces/Action'
import Task from 'interfaces/Task'


interface Props {
  parameters: AutoCover['parameters']
  addTask: (task: Task) => void
}



const AutoCover = (props: Props) => {
  return (
      <form>{ props.parameters }</form>
  )
}

export { AutoCover }
