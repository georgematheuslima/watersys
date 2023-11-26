import React from 'react'
import { Login_page } from './assets/Pages/login_page'
import { BrowserRouter as Router, Route,Routes  } from 'react-router-dom';
import { Cadastro_Usuario } from './assets/Pages/cad_usuario';
import PrivateRoute from './context/PrivateRoute/privateRoute';
import Dashboard from './assets/Pages/Dash/Dashboard';
import { AuthProvider } from './context/AuthProvider/AuthContext';
import { Editar_Usuario } from './assets/Pages/editarUsuario';


export const App = () => {
  return (
    <AuthProvider>
    <Router>
      <Routes>
        <Route path="/cadastroUsuario" element={<Cadastro_Usuario/>} />
        <Route path="/" element={<Login_page/>} />
        <Route path="/verifyUser" element={<PrivateRoute/>}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path='/edit/:userId' element={<Editar_Usuario/>}/>
        </Route>
      </Routes>
    </Router>
    </AuthProvider>
  )
}
