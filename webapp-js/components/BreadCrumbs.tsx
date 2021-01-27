import React from 'react'

import Action from 'interfaces/Action'

interface Props {
  action: Action
  children?: JSX.Element
}

export default (props: Props) =>
  <>
    <nav><h3>{props.action.name}</h3></nav>
    {props.children}
  </>
