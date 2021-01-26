import React from 'react'

import Action from 'interfaces/Action'


interface Props {
  actions: Array<Action>
  setAction: (action: Action|null) => void
}


export default (props: Props) =>
  <ul>
    {props.actions.map(action =>
      <li key={action.name} onClick={() => props.setAction(action)}>
        <a>{ action.name }</a>
      </li>
    )}
  </ul>
