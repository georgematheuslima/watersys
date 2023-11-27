import axios, { AxiosResponse } from 'axios';
import { createContext, useContext,ReactNode, FC, useState  } from 'react';
// import { axiosInstance } from '../services/Api';
type childrenType = {
    children: ReactNode
}


type authContextData = {//
  cadastroUserStatus:boolean;
  EditarUserStatus:boolean;
  cadastroProdutoStatus:boolean;
  //---------------------usuario---------------------
	Login:(email: string, password:string)=> void
  RegistrarUsuario:( name: string, last_name:string, email:string,password:string,phone_number:string,is_admin:boolean )=>void
  GetUsuario:(userId: number)=>void
  GetAllUsuario:() => Promise<AxiosResponse<any>>;
  DeleteUsuario:(userId: number)=>void
  EditarUsuario:(name: string, last_name:string, email:string,password:string,phone_number:string,is_admin:boolean, userId:number)=>void
  //-------------------cliente---------------------
  RegistrarCliente:(email: string, password:string, cpf:string,  phone_number:string)=>void
  //------------------produto---------------------
  RegistrarProduto:( descricao: string, unidade_idunidade:number, valor_compra:number,  valor_venda:number, quantidade:number)=>void
  GetProduto:(produtoId: number)=>void
  AtualizarProduto:(produtoId: number, descricao: string, unidade_idunidade: number, valor_compra: number, valor_venda: number, quantidade: number)=>void
  DeletarProduto:(produtoId: number)=>void
  GetAllProduto:() => Promise<AxiosResponse<any>>;
}

const AuthContext = createContext<authContextData | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
      throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
  };
export const AuthProvider:FC<childrenType> = ({children}) => {
  const [cadastroUserStatus, setcadastroUserStatus] = useState(false);
  const [EditarUserStatus, setEditarUserStatus] = useState(false);

  const [cadastroProdutoStatus, setcadastroProdutoStatus] = useState(false);
  const [EditarProdutoStatus, setEditarProdutoStatus] = useState(false);

  //_-------------------------------------------USUARIO-------------------------------------------------//

	const Login = async (email: string, password:string) => {
      try {
        const response = await axios.post('http://localhost:8000/api/v1/users/login', {
          username: email,
          password: password,
        }, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', 'accept': 'application/json'
            }
        });
        if(response.data){
          const token = response.data.access_token;
          localStorage.setItem('access_token', token);
        }
       
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            console.error('Erro na resposta:', error.response.data);
        } else {
            console.error('Erro no login:', error);
        }
    }
	}

  const RegistrarUsuario = async ( name: string, last_name:string, email:string,password:string,phone_number:string,is_admin:boolean)=>{
    try {
        const response = await axios.post('http://localhost:8000/api/v1/users/signup', {
            name: name,
            last_name: last_name,
            email: email,
            phone_number: phone_number,
            is_admin: is_admin,
            passwd: password,
        }, {
          headers: {
              'Content-Type': 'application/json', 'accept': 'application/json'
          }
      });
    } catch (error:any) {
      setcadastroUserStatus(true);
        console.error('Erro ao registrar usuário:', error.response ? error.response.data : error);
    }
  }

  const EditarUsuario = async ( name: string, last_name:string, email:string,password:string,phone_number:string,is_admin:boolean, userId:number)=>{
    try {
        const response = await axios.put(`http://localhost:8000/api/v1/users/${userId}`, {
            name: name,
            last_name: last_name,
            email: email,
            phone_number: phone_number,
            is_admin: is_admin,
            passwd: password,
        }, {
          headers: {
              'Content-Type': 'application/json', 'accept': 'application/json'
          }
      });
    } catch (error:any) {
      setEditarUserStatus(true);
        console.error('Erro ao Editar usuário:', error.response ? error.response.data : error);
    }
  }

  const GetUsuario = async (userId: number) => {
    try {
        const response = await axios.get(`http://localhost:8000/api/v1/users/${userId}`);
        console.log('Dados do usuário:', response.data);
        return response;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            console.error('Erro ao buscar usuário:', error.response.data);
        } else {
            console.error('Erro na requisição:', error);
        }
    }
  }
  const GetAllUsuario = async () =>{
    try {
      const response = await axios.get("http://localhost:8000/api/v1/users");
      return response;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            console.error('Erro ao buscar usuário:', error.response.data);
        } else {
            console.error('Erro na requisição:', error);
        }
      }
  }

const DeleteUsuario = async (userId: number) => {
  try {
      const response = await axios.delete(`http://localhost:8000/api/v1/users/${userId}`);
      console.log('Usuário deletado com sucesso:', response.data);
  } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
          console.error('Erro ao deletar usuário:', error.response.data);
      } else {
          console.error('Erro na requisição:', error);
      }
  }
}
//_-------------------------------------------CLIENTE-------------------------------------------------//
const RegistrarCliente =(email: string, password:string, cpf:string,  phone_number:string)=>{
  console.log("AQUI");
}
//_-------------------------------------------PRODUTOS-------------------------------------------------//

const RegistrarProduto = async ( descricao: string, unidade_idunidade:number, valor_compra:number,  valor_venda:number, quantidade:number)=>{
  try {
      const response = await axios.post('http://localhost:8000/api/v1/products/product', {
        id:1,
        descricao: descricao,
        unidade_idunidade: unidade_idunidade,
        valor_compra: valor_compra,
        valor_venda: valor_venda,
        quantidade: quantidade,
      },{
        headers: {
            'Content-Type': 'application/json', 'accept': 'application/json'
        }
    });
      console.log("Produto Registrado:"+ response.data);
  } catch (error:any) {
      setcadastroProdutoStatus(true);
      console.error('Erro ao registrar produto:', error.response ? error.response.data : error);
  }
}

const GetProduto = async (produtoId: number) => {
  try {
      const response = await axios.get(`http://localhost:8000/api/v1/products/product/${produtoId}`);
      console.log('Dados do produto:', response.data);
      return response
  } catch (error: any) {
      console.error('Erro ao buscar produto:', error.response ? error.response.data : error);
  }
}

const AtualizarProduto = async (produtoId: number, descricao: string, unidade_idunidade: number, valor_compra: number, valor_venda: number, quantidade: number) => {
  try {
      const response = await axios.put(`http://localhost:8000/api/v1/products/product/${produtoId}`, {
        descricao: descricao,
        unidade_idunidade: unidade_idunidade,
        valor_compra: valor_compra,
        valor_venda: valor_venda,
        quantidade: quantidade,
      },{
        headers: {
            'Content-Type': 'application/json', 'accept': 'application/json'
        }
    });
      console.log('Produto atualizado com sucesso:', response.data);
  } catch (error: any) {
      console.error('Erro ao atualizar produto:', error.response ? error.response.data : error);
  }

}

const DeletarProduto = async (product_id: number) => {
  try {
      const response = await axios.delete(`http://localhost:8000/api/v1/products/product/${product_id}`,{
      });
      console.log('Produto deletado com sucesso:', response.data);
  } catch (error: any) {
      console.error('Erro ao deletar produto:', error.response ? error.response.data : error);
  }
}

const GetAllProduto = async () =>{
  try {
    const response = await axios.get("http://localhost:8000/api/v1/products/products",{});
    return response;
  } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
          console.error('Erro ao buscar Produtos:', error.response.data);
      } else {
          console.error('Erro na requisição:', error);
      }
    }
}



  return (
    <AuthContext.Provider value={{
    Login,
    RegistrarCliente, 
    RegistrarUsuario,
    GetUsuario,
    GetAllUsuario,
    DeleteUsuario,
    EditarUsuario,
    RegistrarProduto,
    GetProduto,
    AtualizarProduto,
    DeletarProduto,
    GetAllProduto,
    cadastroUserStatus,
    EditarUserStatus,
    cadastroProdutoStatus
    }}>
        {children}
    </AuthContext.Provider>
  );
};
