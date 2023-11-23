import React, { createContext, useContext  } from 'react';
// import { axiosInstance } from '../services/Api';
type childrenType = {
    children: React.ReactNode
}
type authContextData = {//
	Login:(email: string, password:string)=> void
  Registrar:(email: string, password:string, cpf:string, contato:string)=>void
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
  const Registrar =(email: string, password:string, cpf:string, contato:string)=>{

  }
  return (
    <AuthContext.Provider value={{Login,Registrar}}>
        {children}
    </AuthContext.Provider>
  )
}