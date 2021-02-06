import * as React from 'react'

import Task from 'interfaces/Task'

import { AutoActionTaskResult } from './actions/AutoActionTaskResult'
import DownloadButton from './DownloadButton'


const TaskResult = (props: {task: Task}) => {

  const { task } = props

  if (task.url.endsWith('.json')) {
    return <AutoActionTaskResult url={task.url} />
  }
  else {
    return <DownloadButton url={task.url} name={task.name} title="result" />
  }
}

export { TaskResult }
