import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { AiOutlineMail,AiOutlineKey } from "react-icons/ai";
import"../scss/Login_Page.scss"
import * as yup from 'yup';
import React from 'react';
import { useAuth } from '../../context/AuthProvider/AuthContext';
type IContactFormProps = {
  email?: string;
  password?: string;
}

const contactSchema = yup.object().shape({
  email: yup.string().email().required(),
  password: yup.string().required(),
});


export const Login_page:React.FC = () => {
	const {Login} = useAuth()
  const { register, handleSubmit, formState } = useForm({
    reValidateMode: 'onBlur',
    resolver: yupResolver(contactSchema),
  });

  const { errors } = formState;

  const onSubmit = (data: IContactFormProps) => {
    Login(String(data.email), String(data.password))
    // console.log(data)
    
  };
  
const ButtomCustom = () =>{
  return(
    <div>
      <button style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Entrar</button>
    </div>
  )
}
  return (
    <div className="background-container">
        <div  className='container_form'>
            <h1 className='loginTxt'>Login</h1>
            <form className='Form' onSubmit={handleSubmit(onSubmit)} >
                <div className='containerInput'>
                    <AiOutlineMail  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="email" placeholder=' Email' {...register('email')}  />
                </div>
                {errors.email && <span className='errorSpan01'>This field is required and must be a valid email</span>}

                <div className='containerInput'>
                    <AiOutlineKey  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="password" placeholder=' Password' {...register('password')} />
                        
                </div>
                
                {errors.password && <span className='errorSpan02'>This field is required and must be a valid email</span>}
                <div className='Container_button'>
                    <ButtomCustom />
                </div>
            </form>
            <div className='Container_Spam'>
                <span className='spam'>Cadastrar Usuário</span><a href='/cadastroUsuario'>Cadastrar Usuário</a>
            </div>
        </div>
  </div>
  )
}
