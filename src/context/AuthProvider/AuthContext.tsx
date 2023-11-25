import axios from 'axios';
import React, { createContext, useContext  } from 'react';
// import { axiosInstance } from '../services/Api';
type childrenType = {
    children: React.ReactNode
}


type authContextData = {//
	Login:(email: string, password:string)=> void
  RegistrarCliente:(email: string, password:string, cpf:string, contato:string)=>void
  RegistrarUsuario:(nome: string, last_name:string, email:string, contato:string, password:string,is_admin:boolean )=>void

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

	const Login = (email: string, password:string) => {
		console.log(email, password)
		// axiosInstance.post("",{email, password})
		// .then(response => {
		// 	console.log(response.data)
		// })
		// .catch(error => {
		// 	console.log(error)
		// });
	}
  const RegistrarCliente =(email: string, password:string, cpf:string, contato:string)=>{
    console.log("AQUI");
  }

  const RegistrarUsuario = async (nome: string, last_name:string, email:string, contato:string, password:string,is_admin:boolean)=>{
    try {
      const response = await axios.post('http://localhost:8000/api/v1/users/signup', {
          nome,
          last_name,
          email,
          contato,
          password,
          is_admin
      });
      console.log(response.data);
      // Outras ações após o registro bem-sucedido, como armazenar tokens, etc.
  } catch (error) {
      console.error('Erro ao registrar usuário:', error);
      // Tratamento de erro apropriado
  }
  }
  return (
    <AuthContext.Provider value={{Login,RegistrarCliente, RegistrarUsuario}}>
        {children}
    </AuthContext.Provider>
  )
}
