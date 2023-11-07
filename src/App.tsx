import React from 'react'
// import { Login_page } from './assets/Pages/login_page'
import { SingUp_page } from './assets/Pages/singUp_page'
import { Login_page } from './assets/Pages/login_page'
import { BrowserRouter as Router, Route,Routes  } from 'react-router-dom';
export const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/cadastro" element={<SingUp_page/>} />
        <Route path="/" element={<Login_page/>} />
      </Routes>
    </Router>
  )
}
