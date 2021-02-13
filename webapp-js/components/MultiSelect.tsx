import React, { useEffect, useState } from 'react'
import * as styles from './MultiSelect.scss'
import DeleteButton from './DeleteButton'

type KV = [string, string]

interface Props {
  options: Array<KV>
  selected: Array<string>
  onChange: (format: Array<string>) => void
}

const MultiSelect = (props: Props) => {

  const [ selected, setSelected ] = useState<Array<KV>>(
    props.options.filter(i => props.selected.indexOf(i[0]) > -1)
  )
  const [ available, setAvailable ] = useState<Array<KV>>(
    props.options.filter(i => props.selected.indexOf(i[0]) === -1)
  )

  useEffect(
    () => {
      setSelected(props.options.filter(i => props.selected.indexOf(i[0]) > -1))
      setAvailable(props.options.filter(i => props.selected.indexOf(i[0]) === -1))
    },
    [props.options, props.selected]
  )

  const addItem = (key: string) => {
    const selectedKeys = selected.map(i => i[0])
    selectedKeys.push(key)
    props.onChange(selectedKeys)
  }

  const removeItem = (key: string) => {
    const selectedKeys = selected.map(i => i[0])
    props.onChange(selectedKeys.filter(i => i !== key))
  }

  return (
    <div className={styles.multiSelect}>
      <ul>
        {selected.map((kv: [string, string]) => {
          const [k, v] = kv
          return (
            <li key={`selected-${k}`}>
              <input
                type="checkbox"
                name={name}
                value={k}
                checked={true}
                readOnly={true}
              />
              {v}&nbsp;<DeleteButton onClick={() => removeItem(k)} />
            </li>
          )
        })}
      </ul>
      <div>
        <select multiple={true} name={`available`} style={{height: 'unset'}}>
          {available.sort().map((kv: [string, string]) => {
            const [k, v] = kv
            return (
              <option
                key={`option-${k}`}
                onClick={() => addItem(k)}
                value={k}
              >
                {v}
              </option>
            )
          })}
        </select>
      </div>
    </div>
  )
}

export { MultiSelect }
