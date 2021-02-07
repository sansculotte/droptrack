import * as React from 'react'

import Task from 'interfaces/Task'

import { AutoActionTaskResult } from './actions/AutoActionTaskResult'
import DownloadButton from './DownloadButton'
import ExpandablePanel from './ExpandablePanel'


const TaskResult = (props: {task: Task}) => {

  const { task } = props

  if (task.url.endsWith('.json')) {
    return <ExpandablePanel><AutoActionTaskResult url={task.url} /></ExpandablePanel>
  }
  else {
    return <DownloadButton url={task.url} name={task.name} title="result" />
  }
}

export { TaskResult }
