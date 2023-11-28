import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { AiOutlineMail,AiOutlineKey, AiTwotoneSchedule, AiOutlinePhone } from "react-icons/ai";
import"../scss/Login_Page.scss"
import * as yup from 'yup';
import React from 'react';
import { useAuth } from '../../context/AuthProvider/AuthContext';
import { useNavigate } from 'react-router-dom';

type IContactFormProps = {
    name?: string;
    last_name?: string;
    email?:string;
     phone_number?:string;
    password:string;
    is_admin?:boolean;
}
const contactSchema= yup.object().shape({
  email: yup.string().required(),
  password: yup.string().required(),
   phone_number:yup.string().required(),
  name:yup.string().required(),
  last_name:yup.string().required(),
  is_admin:yup.boolean()
});


export const Cadastro_Usuario:React.FC = () => {
	const {RegistrarUsuario,cadastroUserStatus} = useAuth()
  const { register, handleSubmit, formState } = useForm({
    reValidateMode: 'onBlur',
    resolver: yupResolver(contactSchema),
  });
  const navigate = useNavigate();

  const { errors } = formState;

  const onSubmit = (data: IContactFormProps) => {
    RegistrarUsuario(String(data.name), String(data.last_name),String(data.email), String(data.password),String(data. phone_number),Boolean(data.is_admin))
    
    if(!cadastroUserStatus){
      setTimeout(() => {
        // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
        alert("A página será recarregada agora.");
      
        // Recarregar a página
        navigate("/verifyUser/dashboard");
      }, 2000);
    }else{
      alert("Usuário não cadastrado");
    }
    
  };
  
const ButtomCustom = () =>{
  return(
    <div>
      <button style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Cadastrar</button>
    </div>
  )
}
  return (
    <div className="background-container">
        <div  className='container_form'>
            <h1 className='loginTxt'>Cadastrar Usuário</h1>
            <form className='Form' onSubmit={handleSubmit(onSubmit)} >

                <div className='containerInput'>
                    <AiTwotoneSchedule  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="text" placeholder='  name' {...register('name')}/>
                </div>
                {errors.name && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiTwotoneSchedule  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="text" placeholder=' Ultimo  name' {...register('last_name')}/>
                </div>
                {errors.last_name && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlineMail  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="email" placeholder=' Email' {...register('email')}  />
                </div>
                {errors.email && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlineKey  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="password" placeholder=' Password' {...register('password')} />
                </div>
                {errors.password && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlinePhone  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='  Contato' {...register('phone_number')}/>
                </div>
                {errors. phone_number && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerCheckbox '>
                    <input type="checkbox" id="is_admin" className="checkboxStyle" {...register('is_admin')}/>
                    <label htmlFor="is_admin">Acesso de Administrador</label>
                </div>

                <div className='Container_button'>
                    <ButtomCustom />
                </div>
            </form>
        </div>
  </div>
  )
}
