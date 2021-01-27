import File from 'interfaces/File'
import * as React from 'react'
import * as styles from './FileList.scss'

import DownloadButton from './DownloadButton'

const fileUrl = (name: string) => `/files/${name}`

export default (props: {files: Array<File>}) =>
  <section className={styles.fileList}>
    <ul>
      {props.files.map((file, index) =>
        <li key={`file_${index}`}>
          <dt>{ file.name }</dt>
          <dd>
            <DownloadButton url={fileUrl(file.name)} name={file.name} title="result" />
          </dd>
        </li>
      )}
    </ul>
  </section>
