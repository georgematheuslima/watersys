import { Navigate, Outlet } from 'react-router-dom';

const PrivateRoute = () => {
    const isAuthenticated = localStorage.getItem('access_token'); // ou outra lógica de autenticação
    console.log("AQUI", isAuthenticated)
    return isAuthenticated ? <Outlet /> : <Navigate to="/" />;
};

export default PrivateRoute;
