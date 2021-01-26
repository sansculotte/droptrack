import React from 'react'
import { AutoEdit } from './AutoEdit'
import { AutoCover } from './AutoCover'

import Action, { AutoEditParameters, AutoCoverParameters } from 'interfaces/Action'
import Task from 'interfaces/Task'


const startAction = (action: Action, addTask: (task: Task) => void) => {
  switch (action.name) {
    case 'autoedit':
      return <AutoEdit
        parameters={action.parameters as AutoEditParameters}
        addTask={addTask}
      />
    case 'autocover':
      return <AutoCover
        parameters={action.parameters as AutoCoverParameters}
        addTask={addTask}
      />
  }
}

export { startAction }
