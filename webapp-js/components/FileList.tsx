import File from 'interfaces/File'
import * as React from 'react'
import * as styles from './FileList.scss'


export default (props: {files: Array<File>}) => {
  return (
    <ul className={styles.fileList}>
      {props.files.map(file => <li>{ file.name }</li>)}
    </ul>
  )
}
