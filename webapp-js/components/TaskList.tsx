import * as React from 'react'

import Task from 'interfaces/Task'
import DownloadButton from './DownloadButton'

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
          <dd>{
            (t.status === 'done' && t.url) &&
              <DownloadButton url={t.url} name={t.name} title="result" />
            }
          </dd>
        </li>
      )}
    </ul>
  </section>
