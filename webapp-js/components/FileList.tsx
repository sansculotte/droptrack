import File from 'interfaces/File'
import * as React from 'react'
import * as styles from './FileList.scss'


export default (props: {files: Array<File>}) => {
  return (
    <ul className={styles.fileList}>
      {props.files.map((file, index) =>
        <li key={`file_${index}`}>{ file.name }</li>)
      }
    </ul>
  )
}
