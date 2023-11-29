import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthProvider/AuthContext';
import"../../scss/Tabela.scss"

const Dashboard_Cliente = () => {


  type IContactFormProps = {
    id:number,
    client_first_name?: string;
    client_last_name?: string;
    cpf?:string;
    phone_number:string;
    email?:string;
    address?:Iaddress
}

type Iaddress={
    address: string,
    type: string,
    state: string,
    abbreviation: string,
    city: string,
    neighborhood: string,
    reference_point: string
}


  const [clientes, setClientes] = useState<IContactFormProps[]>([]);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState('');
    
    const { GetAllCliente,DeletarCliente } = useAuth();
    const navigate = useNavigate();

    function PainelUsuario(){
        navigate('/verifyUser/dashboard')
    }
    
    function PainelProduto(){
      navigate('/verifyUser/dashboardproduto')
    }

    function CadastroCliente(){
        navigate('/verifyUser/cadastroCliente')
    }

    function PAINELVenda(){
      navigate('/verifyUser/dashboardVendas')
  }

    const ButtomCustomCreate = () =>{
      return(
        <div>
          <button onClick={PainelUsuario} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Painel de Usuários</button>
        </div>
      )
    }

    const ButtomCustomCreateProduct = () =>{
      return(
        <div>
          <button onClick={PainelProduto} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Painel de Produto</button>
        </div>
      )
    }

    const ButtomCadastroCliente = () =>{
        return(
          <div>
            <button onClick={CadastroCliente} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Cadastrar Cliente</button>
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
        DeletarCliente(id);
        setTimeout(()=>{
          window.location.reload();
       },2000)
    }

    useEffect(() => {
        const buscarTodosUsuarios = async () => {
            setCarregando(true);
            try {
                const response = await GetAllCliente();
                setClientes(response.data); // Atualizar o estado com os dados recebidos
                setErro(''); // Limpar qualquer erro anterior
            } catch (error) {
                setErro('Erro ao buscar usuários'); // Definir mensagem de erro
            } finally {
                setCarregando(false); // Indicar que o carregamento terminou
            }
        };

        buscarTodosUsuarios();
    }, [GetAllCliente]);

    
    return (
        <div className='container'>
            <div className="container-tabela">
                <h3 className="text-center">Painel de Cliente</h3>
                {carregando && <p>Carregando...</p>}
                {erro && <p>{erro}</p>}
                <table className="table"style={{ marginTop: 20 }}>
                <thead>
                    <tr>
                            <th>ID</th>
                        <th>Primeiro Nome</th>
                        <th>Ultimo nome</th>
                        <th>Telefone</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    {clientes.map((cliente, index) => (
                        <tr key={index}>
                            <td>{cliente.id}</td>
                            <td>{cliente.client_first_name}</td>
                            <td>{cliente.client_last_name}</td>
                            <td>{cliente.phone_number}</td>
                            <td>{cliente.email}</td>
                            <td>
                                <Link to={`/verifyUser/cliente/edit/${cliente.id}`} className="btn btn-primary">
                                Edit
                                </Link>
                            </td>
                            <td>
                                <button onClick={() => Delete(cliente.id)} className="btn btn-danger">
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
                <ButtomCadastroCliente/>
                <ButtomPAINELVendas/>
            </div>
        </div>
    );
};

export default Dashboard_Cliente;
