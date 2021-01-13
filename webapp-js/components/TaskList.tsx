import * as React from 'react'

import Task from 'interfaces/Task'


interface Props {
  tasks: Map<string, Task>
}


export default (props: Props) =>
  <section>
    <ul>
      {Array.from(props.tasks.values()).map(t =>
        <li key={t.uuid}>{ t.name }{ t.status === 'done' && <a href={t.url}>result</a>}</li>)
      }
    </ul>
  </section>
