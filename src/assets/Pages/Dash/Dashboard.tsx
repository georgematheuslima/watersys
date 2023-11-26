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
    const [isReady, setisReady] = useState(false);
    const [erro, setErro] = useState('');
    
    const { GetAllUsuario,DeleteUsuario } = useAuth();
    const navigate = useNavigate();

    function CadastrarUsuario(){
        console.log(usuarios);
        navigate('/cadastroUsuario')
      }
    
    const ButtomCustomRemove = () =>{
      return(
        <div>
          <button onClick={CadastrarUsuario} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Cadastrar Usuário</button>
        </div>
      )
    }

    const Delete = (id:number)=>{
       DeleteUsuario(id);
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

    setTimeout(() => {
      if (!isReady) {
        toastr.info(
          "It is possible that the service is being restarted, please wait more ...",
          "",
          { timeOut: 8000 }
        );
      }

    }, 2000);

    

    return (
      <div className="container-tabela">
      <h3 className="text-center">Lista de Usuários</h3>
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
                        <Link to={`/edit/${usuario.id}`} className="btn btn-primary">
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
      <ButtomCustomRemove/>
  </div>
    );
};

export default Dashboard;
