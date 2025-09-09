import React, { useEffect, useState } from 'react'
import Editor from './components/Editor'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function App() {
  const [token, setToken] = useState('')
  const [docs, setDocs] = useState([])
  const [email, setEmail] = useState('user@example.com')
  const [name, setName] = useState('User')
  const [password, setPassword] = useState('changeme')
  const [selected, setSelected] = useState(null)

  async function register() {
    await fetch(`${API}/auth/register`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, name, password})
    })
  }
  async function login() {
    const res = await fetch(`${API}/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, name, password})
    })
    const data = await res.json()
    setToken(data.access_token)
  }
  async function loadDocs() {
    const res = await fetch(`${API}/documents`, {
      headers: {'Authorization': `Bearer ${token}`}
    })
    const data = await res.json()
    setDocs(data)
  }
  async function createDoc() {
    const res = await fetch(`${API}/documents`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
      body: JSON.stringify({title: 'מסמך חדש', content_json: '{}' })
    })
    const data = await res.json()
    setDocs([data, ...docs])
    setSelected(data)
  }

  useEffect(() => {
    if (token) loadDocs()
  }, [token])

  return (
    <div className="container">
      <h1>דוקס שיתופי – MVP</h1>

      {!token && (
        <div style={{display:'grid', gap:8, maxWidth:400}}>
          <input placeholder='Email' value={email} onChange={e=>setEmail(e.target.value)} />
          <input placeholder='Name' value={name} onChange={e=>setName(e.target.value)} />
          <input placeholder='Password' type='password' value={password} onChange={e=>setPassword(e.target.value)} />
          <div style={{display:'flex', gap:8}}>
            <button onClick={register}>Register</button>
            <button onClick={login}>Login</button>
          </div>
        </div>
      )}

      {token && (
        <>
          <div style={{margin:'12px 0', display:'flex', gap:8}}>
            <button onClick={createDoc}>+ מסמך חדש</button>
            <button onClick={loadDocs}>רענן</button>
          </div>

          <div style={{display:'grid', gridTemplateColumns:'1fr 2fr', gap:16}}>
            <div>
              <h3>המסמכים שלי</h3>
              <ul>
                {docs.map(d => (
                  <li key={d.id}>
                    <button onClick={()=>setSelected(d)}>{d.title}</button>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              {selected ? <Editor token={token} doc={selected} api={API} /> : <p>בחר/י מסמך מהרשימה</p>}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
