

interface Props {
    name: string,
    role:string
}

function NameCard({name, role}: Props) {
  return (
    <div className='p-4 ring-2 rounded-xl bg-blue-600 text-white text-xl font-bold
        flex flex-col'>
        <h1>Welcome, {name}!</h1>
        <div><p className='text-xs'>{role}</p></div>
    </div>
  )
}

export default NameCard
