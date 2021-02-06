import * as React from 'react'

import Task from 'interfaces/Task'

import { TaskResult } from './TaskResult'
import Pulse from './Pulse'

import * as style from './TaskList.scss'


interface Props {
  tasks: Map<string, Task>
}


export default (props: Props) =>
  <section>
    <ul className={style.taskList}>
      {Array.from(props.tasks.values()).map(task =>
        <li key={task.uuid}>
          <dt>{ task.name }</dt>
          <dd>
          {
            task.status === 'done'
            ? <TaskResult task={task} />
            : <Pulse /> 
          }
          </dd>
        </li>
      )}
    </ul>
  </section>
