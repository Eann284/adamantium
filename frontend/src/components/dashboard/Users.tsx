import React from 'react'
import type { User } from '@/src/types/user'

interface Props {
    users: User[]
}

function Users(
   {users}:Props
) {

    
  return (
    <section>
      {users.map(user=>(
        <div key={user.id}>
            <h1>{user.name}</h1>
            <h1>{user.email}</h1>

        </div>
      ))}
    </section>
  )
}

export default Users
