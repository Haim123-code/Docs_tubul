import React, { useEffect, useRef, useState } from 'react'

export default function Editor({ token, doc, api }) {
  const [content, setContent] = useState(doc.content_json || '{}')
  const wsRef = useRef(null)

  useEffect(() => {
    setContent(doc.content_json || '{}')
    const ws = new WebSocket(`ws://localhost:8000/ws/docs/${doc.id}`)
    ws.onmessage = (ev) => {
      // MVP: מקבל טקסט ומעדכן locally
      setContent(ev.data)
    }
    wsRef.current = ws
    return () => ws.close()
  }, [doc.id])

  async function save() {
    await fetch(`${api}/documents/${doc.id}`, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
      body: JSON.stringify({content_json: content})
    })
  }

  function broadcast() {
    wsRef.current?.send(content)
  }

  return (
    <div>
      <h3>{doc.title}</h3>
      <textarea
        value={content}
        onChange={e=>setContent(e.target.value)}
        rows={18}
        style={{width:'100%', fontFamily:'monospace'}}
      />
      <div style={{display:'flex', gap:8, marginTop:8}}>
        <button onClick={save}>שמירה</button>
        <button onClick={broadcast}>שידור שינוי (WS)</button>
      </div>
      <p style={{opacity:0.7, fontSize:12}}>MVP: עריכה כטקסט JSON. ניתן להחליף לעורך עשיר (TipTap/Slate).</p>
    </div>
  )
}
