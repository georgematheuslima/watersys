import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../../context/AuthProvider/AuthContext';
import"../../scss/Tabela.scss"

const Dashboard_Produto = () => {
  interface  IContactFormDTO{
    id:number;
    descricao?: string;
    unidade_idunidade?: number;
    valor_compra?:number;
    valor_venda?:number;
    quantidade:number;
  }

  const [produtos, setProdutos] = useState<IContactFormDTO[]>([]);
    const [carregando, setCarregando] = useState(false);
    const [isReady, setisReady] = useState(false);
    const [erro, setErro] = useState('');
    
    const { GetAllProduto,DeletarProduto } = useAuth();
    const navigate = useNavigate();

    function CadastrarUsuario(){
        navigate('/cadastroUsuario')
    }
    
    function CadastrarProduto(){
      navigate('/verifyUser/cadastroProduto')
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
          <button onClick={CadastrarProduto} style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Cadastrar Produto</button>
        </div>
      )
    }


    const Delete = (id:number)=>{
        DeletarProduto(id);

       
    }
    useEffect(() => {
        const buscarTodosUsuarios = async () => {
            setCarregando(true);
            try {
                const response = await GetAllProduto();
                console.log(response.data)
                setProdutos(response.data); // Atualizar o estado com os dados recebidos
                setErro(''); // Limpar qualquer erro anterior
            } catch (error) {
                setErro('Erro ao buscar usuários'); // Definir mensagem de erro
            } finally {
                setCarregando(false); // Indicar que o carregamento terminou
            }
        };

        buscarTodosUsuarios();
    }, [GetAllProduto]);

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
      <h3 className="text-center">Lista de Produtos</h3>
      {carregando && <p>Carregando...</p>}
      {erro && <p>{erro}</p>}
      <table className="table"style={{ marginTop: 20 }}>
          <thead>
              <tr>
                    <th>ID</th>
                  <th>Descrição</th>
                  <th>ID Unidade</th>
                  <th>Quantidade</th>
                  <th>Valor da compra</th>
                  <th>Valor da venda</th>
              </tr>
          </thead>
          <tbody>
              {produtos.map((produto, index) => (
                  <tr key={index}>
                      <td>{produto.id}</td>
                      <td>{produto.descricao}</td>
                      <td>{produto.unidade_idunidade}</td>
                      <td>{produto.quantidade}</td>
                      <td>{produto.valor_compra}</td>
                      <td>{produto.valor_venda}</td>
                      <td>
                        <Link to={`/verifyUser/produto/edit/${produto.id}`} className="btn btn-primary">
                          Edit
                        </Link>
                      </td>
                      <td>
                        <button onClick={() => Delete(produto.id)} className="btn btn-danger">
                          Delete
                        </button>
                      </td>
                  </tr>
              ))}
          </tbody>
      </table>
      <ButtomCustomCreate/>
      <ButtomCustomCreateProduct/>
  </div>
    );
};

export default Dashboard_Produto;
