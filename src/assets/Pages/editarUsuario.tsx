import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { AiOutlineMail,AiOutlineKey, AiTwotoneSchedule, AiOutlinePhone } from "react-icons/ai";
import"../scss/Login_Page.scss"
import * as yup from 'yup';
import React, { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthProvider/AuthContext';
import { useNavigate, useParams } from 'react-router-dom';

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


export const Editar_Usuario:React.FC = () => {
  const [usuario, setUsuario] = useState("");
  const [erro, setErro] = useState('');
  const [carregando, setCarregando] = useState(false);
  const {EditarUsuario,EditarUserStatus,GetUsuario} = useAuth()
  const { register, handleSubmit, formState,setValue } = useForm({
    reValidateMode: 'onBlur',
    resolver: yupResolver(contactSchema),
  });
  const { userId } = useParams();
  const { errors } = formState;
  const navigate = useNavigate();

  useEffect(() => {
    const buscarTodosUsuarios = async () => {
        setCarregando(true);
        try {
            const response = await GetUsuario(Number(userId));
            setUsuario(response.data.name);
            setValue('email',response.data.email);
            setValue('name', response.data.name);
            setValue('last_name', response.data.last_name);
            setValue('phone_number', response.data.phone_number);
            setValue('is_admin', response.data.is_admin);
            setErro(''); // Limpar qualquer erro anterior
        } catch (error) {
            setErro('Erro ao buscar usuários'); // Definir mensagem de erro
        } finally {
            setCarregando(false); // Indicar que o carregamento terminou
        }
    };

    buscarTodosUsuarios();
}, [GetUsuario]);


  const onSubmit = (data: IContactFormProps) => {
    EditarUsuario(String(data.name), String(data.last_name),String(data.email), String(data.password),String(data. phone_number),Boolean(data.is_admin), Number((userId)))
    if(!EditarUserStatus){
      setTimeout(() => {
        // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
        alert("A página será recarregada agora.");
      
        // Recarregar a página
        navigate("/verifyUser/dashboard");
      }, 2000);
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
            <h1 className='loginTxt'>Editar Usuário</h1>
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
