import axios from 'axios';
import React, { createContext, useContext  } from 'react';
// import { axiosInstance } from '../services/Api';
type childrenType = {
    children: React.ReactNode
}


type authContextData = {//
  //usuario
	Login:(email: string, password:string)=> void
  RegistrarUsuario:( name: string, last_name:string, email:string,  phone_number:string, password:string,is_admin:boolean )=>void
  GetUsuario:(userId: string)=>void
  DeleteUsuario:(userId: string)=>void
    //cliente
  RegistrarCliente:(email: string, password:string, cpf:string,  phone_number:string)=>void
    //produto
}

const AuthContext = createContext<authContextData | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
      throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
  };
export const AuthProvider:React.FC<childrenType> = ({children}) => {


  //_-------------------------------------------USUARIO-------------------------------------------------//

	const Login = async (email: string, password:string) => {
      console.log(email, password)
      try {
        const response = await axios.post('http://localhost:8000/api/v1/users/login', {
            username: email,
            password: password
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('Login bem-sucedido:', response.data);
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            console.error('Erro na resposta:', error.response.data);
        } else {
            console.error('Erro no login:', error);
        }
    }
	}

  const RegistrarUsuario = async ( name: string, last_name:string, email:string,  phone_number:string, password:string,is_admin:boolean)=>{
      
    try {
        const response = await axios.post('http://localhost:8000/api/v1/users/signup', {
            name: name,
            last_name: last_name,
            email: email,
            phone_number: phone_number,
            passwd: password,
            is_admin: is_admin
        });
        console.log(response.data);
    } catch (error:any) {
        console.error('Erro ao registrar usuário:', error.response ? error.response.data : error);
    }
  }

  const GetUsuario = async (userId: string) => {
    try {
        const response = await axios.get(`http://localhost:8000/api/v1/users/${userId}`);
        console.log('Dados do usuário:', response.data);
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            console.error('Erro ao buscar usuário:', error.response.data);
        } else {
            console.error('Erro na requisição:', error);
        }
    }
}

const DeleteUsuario = async (userId: string) => {
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
        descricao: descricao,
        unidade_idunidade: unidade_idunidade,
        valor_compra: valor_compra,
        valor_venda: valor_venda,
        quantidade: quantidade,
      });
      console.log(response.data);
  } catch (error:any) {
      console.error('Erro ao registrar produto:', error.response ? error.response.data : error);
  }
}
  return (
    <AuthContext.Provider value={{Login,RegistrarCliente, RegistrarUsuario,GetUsuario,DeleteUsuario}}>
        {children}
    </AuthContext.Provider>
  )
}
