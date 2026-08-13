'use client';
import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";

interface Login {
    email: string
    password: string
}

function LoginPage() {

    const [loading, setLoading] = useState(false);
    const router = useRouter();
    const {
        register, handleSubmit, formState: {errors}
    } = useForm<Login>()


    const onSubmit = async(data: Login)=>{
        setLoading(true);
        try {
            const result = await signIn('credentials', {
                email: data.email,
                password: data.password,
                redirect:false
            })

            if (result?.error) {
                toast.error('Invalid email or password')
            } else {
                toast.success('Logged in')
                router.push('/dashboard')
            }

        } catch (error) {
            toast.error('Error')
            console.error(error)
        } finally {
            setLoading(false)
        }
    }

  return (
    <main className="flex flex-1 h-screen items-center justify-center p-4 gap-2">
      <form onSubmit={handleSubmit(onSubmit)} className="ring ring-gray-400 w-100 h-full p-4">
        <div>

            <h1 className="w-full text-center text-lg font-semibold mb-3">Inventory Management</h1>
            <section className="flex flex-col gap-1">


            <label className="font-semibold">Email</label>
            <input 
             {...register('email', {
               required: 'Email is required',
               pattern: {
                 value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                 message: 'Invalid email address',
                },
              })}
              
              
              type="email" placeholder="Email" className="ring ring-gray-400 rounded-md px-2 py-1"/>
            </section>
            {errors.email && (
              <p className="text-red-500 text-sm mt-1 mb-1">{errors.email.message}</p>
            )}
            
            <section className="flex flex-col gap-1 mt-2">

            <label htmlFor="" className="font-semibold">Password</label>
             <input 
             {...register('password', {
               required: 'Password is required',
              
              })}
              
              
              type="password" placeholder="Password" className="ring ring-gray-400 rounded-md px-2 py-1"/>
            
            </section>
            {errors.password && (
              <p className="text-red-500 text-sm mt-1 mb-1">{errors.password.message}</p>
            )}

            <button type="submit" className="w-full bg-blue-500 text-white font-semibold rounded-md py-1 mt-2">
                {loading ? 'Logging in...': 'Log In'}
            </button>
        </div>
      </form>
    </main>
  )
}

export default LoginPage
