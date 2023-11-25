import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { AiOutlineMail,AiOutlineKey, AiTwotoneSchedule, AiOutlinePhone } from "react-icons/ai";
import"../scss/Login_Page.scss"
import * as yup from 'yup';
import React from 'react';
import { useAuth } from '../../context/AuthProvider/AuthContext';
type IContactFormProps = {
  email?: string;
  password?: string;
  cpf?:string;
   phone_number:string;
}

interface  IContactFormDTO{
    email?: string;
    password?: string;
    cpf?:string;
     phone_number?:string;
  }

const contactSchema= yup.object().shape({
  email: yup.string().required(),
  password: yup.string().required(),
   phone_number:yup.string().required(),
  cpf:yup.string().required(),


});


export const Cadastro_page:React.FC = () => {
	const {RegistrarCliente} = useAuth()
  const { register, handleSubmit, formState } = useForm({
    reValidateMode: 'onBlur',
    resolver: yupResolver(contactSchema),
  });

  const { errors } = formState;

  const onSubmit = (data: IContactFormProps) => {
    RegistrarCliente(String(data.email), String(data.password),String(data.cpf), String(data. phone_number))
    // console.log(data)
    
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
            <h1 className='loginTxt'>Cadastrar Cliente</h1>
            <form className='Form' onSubmit={handleSubmit(onSubmit)} >
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
                    <AiTwotoneSchedule  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder=' CPF' {...register('cpf')}/>
                </div>
                {errors.cpf && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlinePhone  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='  phone_number' {...register('phone_number')}/>
                </div>
                {errors. phone_number && <span className='errorSpan01'>Preencha todos os campos</span>}


                <div className='Container_button'>
                    <ButtomCustom />
                </div>
            </form>
        </div>
  </div>
  )
}
