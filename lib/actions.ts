'use server'
import { Provider } from "@supabase/supabase-js"
import { createClientForServer } from "./supabase/server"
import { redirect } from "next/navigation"

const signInWith = (provider: Provider) => async() => {
   const supabase = await createClientForServer()

   const auth_callback_url = `${process.env.NEXTAUTH_URL}/auth/callback`

   const {data, error} = 
   await supabase.auth.signInWithOAuth({
    provider,
    options: {
        redirectTo: auth_callback_url,
        queryParams: {
            access_type: 'offline',
            prompt: 'consent',
        },
    },
   })

   console.log(data)

   if (error) {
    console.log(error)
   }
   if (!data?.url) {
    console.error("No redirect URL returned from Supabase.")
    return
   }
   redirect(data.url)
}

const signInWIthGoogle = signInWith('google')

const signOut = async() => {
    const supabase = await createClientForServer()
    await supabase.auth.signOut()
}

export {signInWIthGoogle, signOut}