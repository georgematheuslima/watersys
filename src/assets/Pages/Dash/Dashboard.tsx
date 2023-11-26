import React from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
    const navigate = useNavigate();

    function removeToken(){
        localStorage.removeItem('access_token');
        navigate('/');

      }
    
    const ButtomCustomRemove = () =>{
        return(
          <div>
            <button onClick={removeToken} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Logout</button>
          </div>
        )
      }
    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="dashboard-content">
                {/* Conteúdo do dashboard aqui */}
                <p>Bem-vindo ao seu dashboard!</p>
                {/* Você pode adicionar mais componentes e conteúdos aqui, como gráficos, tabelas, etc. */}
                <div className='Container_button'>
                    <ButtomCustomRemove />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
