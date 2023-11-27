import React from 'react'
import { Login_page } from './assets/Pages/login_page'
import { BrowserRouter as Router, Route,Routes  } from 'react-router-dom';
import { Cadastro_Usuario } from './assets/Pages/cad_usuario';
import PrivateRoute from './context/PrivateRoute/privateRoute';
import Dashboard from './assets/Pages/Dash/Dashboard';
import { AuthProvider } from './context/AuthProvider/AuthContext';
import { Editar_Usuario } from './assets/Pages/editarUsuario';
import { Cadastro_Produto } from './assets/Pages/produto/cad_produto';
import Dashboard_Produto from './assets/Pages/produto/Dashboard_produto';
import { Editar_Produto } from './assets/Pages/produto/edit_produto';
import Dashboard_Cliente from './assets/Pages/client/DashboardCliente';
import { Cadastro_Cliente } from './assets/Pages/client/cad_cliente';
import { Edita_Cliente } from './assets/Pages/client/edit_cliente';


export const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/cadastroUsuario" element={<Cadastro_Usuario/>} />
          <Route path="/" element={<Login_page/>} />
          <Route path="/verifyUser/" element={<PrivateRoute/>}>
            <Route path="dashboard" element={<Dashboard />} />
            {/* PRODUTO */}
            <Route path="edit/:userId" element={<Editar_Usuario/>}/>
            <Route path="cadastroProduto" element={<Cadastro_Produto/>}/>
            <Route path="dashboardproduto" element={<Dashboard_Produto/>}/>
            <Route path="produto/edit/:produtoId" element={<Editar_Produto/>}/>
            {/* CLIENTE */}
            <Route path="dashboardcliente" element={<Dashboard_Cliente/>}/>
            <Route path="cadastroCliente" element={<Cadastro_Cliente/>}/>
            <Route path="cliente/edit/:clienteId" element={<Edita_Cliente/>}/>

          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  )
}
