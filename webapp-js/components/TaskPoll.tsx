import http from 'lib/http'
import * as React from 'react'
import { useState } from 'react'
import { useInterval } from '../hooks/useInterval'
import Task from 'interfaces/Task'


interface Props {
  tasks: Map<string, Task>
  updateTasks: (tasks: Map<string, Task>) => void
  flashMessage: (message: string) => void 
}

const activeTasks = (tasks: Map<string, Task>) =>
    new Map([...tasks].filter(([_, t]) => t.status === 'processing'))

export default (props: Props) => {

  const [ color, setColor ] = useState('#000')

  const ping = () => {
    setColor('#ac0000')
    setTimeout(() => setColor('#000000'), 200)
  }

  const pollTasks = async () => {
    const { tasks } = props
    activeTasks(tasks).forEach(async (t) => {
        const response = await http.poll(`/tasks/${t.uuid}`)
        const task = response.data
        if (task.status === 'done') {
          props.flashMessage(`Task ${task.name} has finished!`)
        }
        tasks.set(t.uuid, task)
    })
    ping()
    props.updateTasks(tasks)
  }

  useInterval(pollTasks, 10000)


  return (
    <div style={
      {
        position: 'relative',
        top: '-2px',
        width: '20px',
        height: '20px',
        borderRadius: '50%',
        backgroundColor: color,
        transition: 'background-color 50ms ease-in, 300ms ease-out',
        float: 'right',
      }
    }><div style={
        {
            color: 'white',
            position: 'absolute',
            left: 'calc(50% - 3px)',
            top: 'calc(50% - 4px)',
            fontSize: '10px'
        }
    }>{activeTasks(props.tasks).size}</div></div>
  )
}
