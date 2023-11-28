import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthProvider/AuthContext';
import"../../scss/Tabela.scss"

const Dashboard = () => {
  interface  IContactFormDTO{
    id:number;
    name?: string;
    last_name?: string;
    email?:string;
    phone_number?:string;
    password:string;
    is_admin:boolean;
  }

  const [usuarios, setUsuarios] = useState<IContactFormDTO[]>([]);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState('');
    
    const { GetAllUsuario,DeleteUsuario } = useAuth();
    const navigate = useNavigate();

    function CadastrarUsuario(){
        navigate('/cadastroUsuario')
    }
    
    function PainelProdutos(){
      navigate('/verifyUser/dashboardproduto')
    }

    function PainelCliente(){
      navigate('/verifyUser/dashboardcliente')
    }

    function PAINELVenda(){
      navigate('/verifyUser/dashboardVendas')
  }
    const ButtomCustomCreate = () =>{
      return(
        <div>
          <button onClick={CadastrarUsuario} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Cadastrar Usuário</button>
        </div>
      )
    }

    const ButtomCustomCreateProduct = () =>{
      return(
        <div>
          <button onClick={PainelProdutos} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Painel de Produtos</button>
        </div>
      )
    }

    const ButtomCustomCreateCliente = () =>{
      return(
        <div>
          <button onClick={PainelCliente} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Painel Cliente</button>
        </div>
      )
    }

    const ButtomPAINELVendas = () =>{
      return(
        <div>
          <button onClick={PAINELVenda} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Painel de Vendas</button>
        </div>
    )
  }


    const Delete = (id:number)=>{
       DeleteUsuario(id);

       setTimeout(()=>{
          window.location.reload();
       },2000)
    }
    useEffect(() => {
        const buscarTodosUsuarios = async () => {
            setCarregando(true);
            try {
                const response = await GetAllUsuario();
                console.log(response.data)
                setUsuarios(response.data); // Atualizar o estado com os dados recebidos
                setErro(''); // Limpar qualquer erro anterior
            } catch (error) {
                setErro('Erro ao buscar usuários'); // Definir mensagem de erro
            } finally {
                setCarregando(false); // Indicar que o carregamento terminou
            }
        };

        buscarTodosUsuarios();
    }, [GetAllUsuario]);

    
    return (
      <div className='container'>
        <div className="container-tabela">
          <h3 className="text-center">Painel de Usuários</h3>
          {carregando && <p>Carregando...</p>}
          {erro && <p>{erro}</p>}
          <table className="table"style={{ marginTop: 20 }}>
              <thead>
                  <tr>
                      <th>Name</th>
                      <th>Last Name</th>
                      <th>Contact</th>
                      <th>Admin</th>
                  </tr>
              </thead>
              <tbody>
                  {usuarios.map((usuario, index) => (
                      <tr key={index}>
                          <td>{usuario.name}</td>
                          <td>{usuario.last_name}</td>
                          <td>{usuario.phone_number}</td>
                          <td>{usuario.is_admin ? 'Yes' : 'No'}</td>
                          <td>
                            <Link to={`/verifyUser/edit/${usuario.id}`} className="btn btn-primary">
                              Edit
                            </Link>
                          </td>
                          <td>
                            <button onClick={() => Delete(usuario.id)} className="btn btn-danger">
                              Delete
                            </button>
                          </td>
                      </tr>
                  ))}
              </tbody>
          </table>
          
        </div>
        <div className='buttonFoot'>
          <ButtomCustomCreate/>
          <ButtomCustomCreateProduct/>
          <ButtomCustomCreateCliente/>
          <ButtomPAINELVendas/>
        </div>
      </div>
    );
};

export default Dashboard;
