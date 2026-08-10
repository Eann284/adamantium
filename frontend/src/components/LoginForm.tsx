// import { useState } from "react"


function LoginForm() {

    // TODO: Create a handleLogin function
    // take user input, send to /auth/login
    // it should return a token i can view using devtools in browser
    // ? am i passing in json?
    

    // *Pseudocode
    // handleLogin = (form_data) => (
        // await api.post(form_data) or something
        
        // ? return user? and Token?
// )

  return (
    <form>
        <label htmlFor="">Email</label>
        <input type="text" />
        <label htmlFor="">Password</label>
        <input type="text" />
    </form>
  )
}

export default LoginForm
