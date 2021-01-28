declare var API_URL: string
import * as React from 'react'

import Task from 'interfaces/Task'
import DownloadButton from './DownloadButton'
import Pulse from './Pulse'


const TaskResult = (props: {task: Task}) => {

  const { task } = props

  switch (task.status) {
    case 'done':
      return <DownloadButton url={task.url} name={task.name} title="result" />
    default:
      return <Pulse />
  }
}

export { TaskResult }
