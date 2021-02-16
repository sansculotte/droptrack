import File from 'interfaces/File'
import * as React from 'react'
import * as styles from './FileList.scss'

import { sortCompare } from 'lib/file'
import http from 'lib/http'
import DeleteButton from './DeleteButton'
import DownloadButton from './DownloadButton'

interface Props {
  files: Array<File>
  onChange: () => void
  flashMessage: (message: string) => void
}

const fileUrl = (name: string) => `/files/${name}`

export default (props: Props) => {

  const deleteFile = async (name: string) => {
    try {
      const result = await http.delete(`files/${name}`)
      props.flashMessage(result.data.message)
      props.onChange()
    }
    catch (e) {
      console.error(e)
    }
  }

  return (
    <section className={styles.fileList}>
      <ul>
        {props.files.sort(sortCompare('name')).map((file, index) =>
          <li key={`file_${index}`}>
            <dt>{ file.name }</dt>
            <dd>
              <DownloadButton url={fileUrl(file.name)} name={file.name} title="result" />
            </dd>
            <dd>
              <DeleteButton onClick={() => deleteFile(file.name)} title="delete" />
            </dd>
          </li>
        )}
      </ul>
    </section>
  )
}
