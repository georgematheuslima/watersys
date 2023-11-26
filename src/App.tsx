import React from 'react'
import { Login_page } from './assets/Pages/login_page'
import { BrowserRouter as Router, Route,Routes  } from 'react-router-dom';
import { Cadastro_Usuario } from './assets/Pages/cad_usuario';
import PrivateRoute from './context/PrivateRoute/privateRoute';
import Dashboard from './assets/Pages/Dash/Dashboard';


export const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/cadastroUsuario" element={<Cadastro_Usuario/>} />
        <Route path="/" element={<Login_page/>} />
        <Route path="/verifyUser" element={<PrivateRoute/>}>
          <Route path="dashboard" element={<Dashboard />} />
        </Route>
      </Routes>
    </Router>
  )
}
