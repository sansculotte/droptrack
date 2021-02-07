import React, { useState } from 'react'

import { expandablePanel } from './ExpandablePanel.scss'

interface Props {
  children: JSX.Element
}


export default (props: Props) => {

  const [ isExpanded, setIsExpanded ] = useState(false)

  return (
    <div className={expandablePanel}>
      <button onClick={() => setIsExpanded(!isExpanded)}>…</button>
      {isExpanded &&
        <div>
          {props.children}
        </div>
      }
    </div>
  )
}
