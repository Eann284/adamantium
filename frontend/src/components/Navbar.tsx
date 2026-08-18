import { Session } from 'next-auth'
import React from 'react'

interface Props {
  session: Session | null;
}

function Navbar({session}:Props) {
  return (
    <nav className='bg-blue-500 h-12 p-3'>
      <h1>Hello, {session?.user.email}</h1>
    </nav>
  )
}

export default Navbar
