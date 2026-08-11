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
    <div>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
            <input 
             {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Invalid email address',
                },
              })}


            type="email" placeholder="Email" />
            
             <input 
             {...register('password', {
                required: 'password is required',
              
              })}
              

            type="password" placeholder="password" />
            
            {errors.password && (
              <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
            )}

            <button type="submit">
                {loading ? 'Logging in...': 'Log In'}
            </button>
        </div>
      </form>
    </div>
  )
}

export default LoginPage
