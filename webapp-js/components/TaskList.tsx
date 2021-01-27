import * as React from 'react'

import Task from 'interfaces/Task'

import { TaskResult } from './TaskResult'

import * as style from './TaskList.scss'


interface Props {
  tasks: Map<string, Task>
}


export default (props: Props) =>
  <section>
    <ul className={style.taskList}>
      {Array.from(props.tasks.values()).map(t =>
        <li key={t.uuid}>
          <dt>{ t.name }</dt>
          <dd><TaskResult task={t} /></dd>
        </li>
      )}
    </ul>
  </section>
