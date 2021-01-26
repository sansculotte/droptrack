import React, { useState } from 'react'

import { startAction } from './Action'
import ActionList from './ActionList'

import Action from 'interfaces/Action'
import Task from 'interfaces/Task'

import * as styles from './Actions.scss'


interface Props {
  actions: Array<Action>
  addTask: (task: Task) => void
}


const ActionPanel = (props: Props) => {

  const [ action, setAction ] = useState<Action|null>(null)

  return (
    <section className={styles.actions}>
      {
      (action === null)
        ? <ActionList actions={props.actions} setAction={setAction} />
        : startAction(action, props.addTask)
      }
    </section>
  )
}

export { ActionPanel }
