import * as React from 'react'

import * as styles from './DeleteButton.scss'

interface Props {
  title?: string
  onClick: (ev: React.MouseEvent<HTMLButtonElement>) => void
}

export default (props: Props) => {
  return (
    <button
      style={{width: '30px', height: '30px'}}
      onClick={props.onClick}
      title={props.title}
      className={styles.deleteButton}
    >🗙</button>
  )
}
