import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthProvider/AuthContext';
import"../../scss/Tabela.scss"

const Dashboard_venda = () => {
    type IContactFormProps = {
        id:number;
        quantity?: number;
        returnable?: boolean;
        product_id?:number;
        cpf?:string;
    }

  const [vendas, setvendas] = useState<IContactFormProps[]>([]);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState('');
    
    const { GetAllVendas, DeletarVenda,registarVendaStatus } = useAuth();
    const navigate = useNavigate();

    function PainelUsuario(){
        navigate('/verifyUser/dashboard')
    }
    
    function PainelCliente(){
      navigate('/verifyUser/dashboardcliente')
    }

    function RegistarVenda(){
      navigate('/verifyUser/registrarVenda')
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
          <button onClick={RegistarVenda} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Fazer venda</button>
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


    const Delete = (id:number)=>{
        DeletarVenda(id);
        if(!registarVendaStatus){
            setTimeout(() => {
              // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
              alert("Usuario DELETADO com SUCESSO");
            
              // Recarregar a página
              navigate("/verifyUser/dashboard");
            }, 2000);
        }else{
            setTimeout(() => {
                // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
                alert("ERRO AO DELETAR USUARIO");
              
                // Recarregar a página
              }, 1000);
        }
       
    }
    useEffect(() => {
        const buscarTodosUsuarios = async () => {
            setCarregando(true);
            try {
                const response = await GetAllVendas();
                console.log(response.data)
                setvendas(response.data); // Atualizar o estado com os dados recebidos
                setErro(''); // Limpar qualquer erro anterior
            } catch (error) {
                setErro('Erro ao buscar usuários'); // Definir mensagem de erro
            } finally {
                setCarregando(false); // Indicar que o carregamento terminou
            }
        };

        buscarTodosUsuarios();
    }, [GetAllVendas]);
    
    return (
      <div className='container'>
        <div className="container-tabela">
          <h3 className="text-center">Painel de Vendas</h3>
          {carregando && <p>Carregando...</p>}
          {erro && <p>{erro}</p>}
          <table className="table"style={{ marginTop: 20 }}>
              <thead>
                  <tr>
                        <th>ID</th>
                      <th>Quantidade</th>
                      <th>CPF Cliente</th>
                      <th>ID PRODUTO</th>
                      <th>Retornavel</th>
                  </tr>
              </thead>
              <tbody>
                {vendas.map((venda, index) => (
                    <tr key={index}>
                        <td>{venda.id}</td>
                        <td>{venda.quantity}</td>
                        <td>{venda.cpf}</td>
                        <td>{venda.product_id}</td>
                        <td>{venda.returnable ? 'Yes' : 'No'}</td>
                        <td>
                        </td>
                        <td>
                          <button onClick={() => Delete(venda.id)} className="btn btn-danger">
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
        </div>
    </div>
  );
};

export default Dashboard_venda;
