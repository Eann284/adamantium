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

      <input type="text" placeholder='search' className='px-2 w-full ring ring-gray-400 rounded-lg'/>
      <table className='w-full'>

      {users.map(user=>(
        <tr key={user.id}>
            <td>{user.name}</td>
            <td>{user.email}</td>

        </tr>
      ))}
      </table>
    </section>
  )
}

export default Users
