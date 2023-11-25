import React from 'react'
// import { Login_page } from './assets/Pages/login_page'
import { Login_page } from './assets/Pages/login_page'
import { BrowserRouter as Router, Route,Routes  } from 'react-router-dom';
import { Cadastro_Usuario } from './assets/Pages/cad_usuario';
export const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/cadastroUsuario" element={<Cadastro_Usuario/>} />
        <Route path="/" element={<Login_page/>} />
      </Routes>
    </Router>
  )
}
