import { createClientForServer } from "@/lib/supabase/server"
import { redirect } from "next/navigation"
import ClientHomePage from "@/app/components/ClientHomePage"

//create country section using ISO 8601 cou try code

export default async function HomePage() {
  const supabase = await createClientForServer()
  // use getUser for server side, and use getSession only for client side
  const session = await supabase.auth.getUser()

  if (!session.data.user)
    redirect("/auth/login")

  // const {
  //   data: {
  //     user: {user_metadata, app_metadata},
  //   },
  // } = session

  // const {name, email, user_name, avatar_url} = user_metadata
  // const userName = user_name? `@{user_name}` : 'User Name Not Set'
  console.log(session)
  return <ClientHomePage/>
}
