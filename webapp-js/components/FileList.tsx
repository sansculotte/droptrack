import * as React from 'react'
import * as styles from './FileList.scss'

interface Props {
    files: Array<string>
}

export default (props: Props) => {
  return (
    <ul className={styles.fileList}>
      {props.files.map(file => <li>{ file }</li>)}
    </ul>
  )
}
