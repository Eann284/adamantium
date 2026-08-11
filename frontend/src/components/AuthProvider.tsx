import { SessionProvider } from "next-auth/react";
import { ReactNode } from "react";
import { Toaster } from "react-hot-toast";

export function AuthProvider({children}:{children: ReactNode}) {
    return(
        <SessionProvider>
            {children}
            <Toaster position="top-right"/>
        </SessionProvider>
    )
}