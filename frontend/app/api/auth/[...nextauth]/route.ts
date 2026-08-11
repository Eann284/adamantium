import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";


const handler = NextAuth({
    providers: [
        CredentialsProvider({
            name: 'Credentials',
            credentials: {
                email:{label: 'Email', type: 'email'},
                password:{label: 'Password', type: 'password'},
            },
            async authorize(credentials) {
                if (!credentials?.email||!credentials?.password) {return null}
                
                const formData = new URLSearchParams({
                    username: credentials.email,
                    password: credentials.password
                })

                const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type':'application/x-www-form-urlencoded',
                    },
                    body: formData
                })

                const data = await res.json()

                if (!res.ok || !data.access_token) {
                return null
                }

                return {
                    id: data.user.id,
                    name: data.user.name,
                    email: data.user.email,
                    role: data.user.role,
                    area: data.user.area,
                    accessToken: data.access_token,
                    }

            }
        })
    ],
    callbacks:{
        async jwt({token,user}) {
            if (user) {
                token.accessToken = user.accessToken
                token.role = user.role
                token.area = user.area
            }
            return token
        },
        async session({ session, token }) {
        session.user.role = token.role as string
        session.user.area = token.area as string
        session.user.accessToken = token.accessToken as string
        return session
        },
    },
    session:{
        strategy: 'jwt',
    },
    pages: {
        signIn: '/login'
    }
})

export {handler as GET, handler as POST}