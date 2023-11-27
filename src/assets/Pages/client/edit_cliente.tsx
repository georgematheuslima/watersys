import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { AiOutlineMail,AiOutlineKey, AiTwotoneSchedule, AiOutlinePhone } from "react-icons/ai";
import"../client/cliente_Page.scss";
import * as yup from 'yup';
import React, { useEffect, useState } from 'react';
import { useAuth } from '../../../context/AuthProvider/AuthContext';
import { useNavigate, useParams } from 'react-router-dom';
type IContactFormProps = {
    client_first_name?: string;
    client_last_name?: string;
    cpf?:string;
    phone_number:string;
    email?:string;
    address:Iaddress
}

type Iaddress={
    id?:number,
    address: string,
    type: string,
    state: string,
    abbreviation: string,
    city: string,
    neighborhood: string,
    reference_point: string
}

const contactSchema= yup.object().shape({
    email: yup.string().required(),
    client_first_name: yup.string().required(),
    client_last_name: yup.string().required(),
    phone_number:yup.string().required(),
    cpf:yup.string().required(),
    address: yup.object().shape({
        address: yup.string().required("Endereço é obrigatório"),
        type: yup.string().required("Tipo de endereço é obrigatório"),
        state: yup.string().required("Estado é obrigatório"),
        abbreviation: yup.string().required("Abreviação é obrigatória"),
        city: yup.string().required("Cidade é obrigatória"),
        neighborhood: yup.string().required("Bairro é obrigatório"),
        reference_point: yup.string().required("Ponto de referência é obrigatório"),
    }),

});


export const Edita_Cliente:React.FC = () => {
	const {AtualizarCliente,GetCliente,EditarClienteStatus} = useAuth()
    const navigate = useNavigate();
    const [erro, setErro] = useState('');
    const { register, handleSubmit, formState,setValue} = useForm({
        reValidateMode: 'onBlur',
        resolver: yupResolver(contactSchema),
    });

    const { clienteId } = useParams();
  const { errors } = formState;


  useEffect(() => {
    const buscarTodosUsuarios = async () => {
        try {
            const response = await GetCliente(Number(clienteId));
            console.log(response.data)
            setValue('client_first_name',response.data.client_first_name);
            setValue('client_last_name', response.data.client_last_name);
            setValue('cpf', response.data.cpf);
            setValue('phone_number', response.data.phone_number);
            setValue('email', response.data.email);
            setValue('address', response.data.address.address);
            setValue('type', response.data.address.type);
            setValue('state', response.data.address.state);
            setValue('abbreviation', response.data.address.abbreviation);
            setValue('city', response.data.address.city);
            setValue('neighborhood', response.data.address.neighborhood);
            setValue('reference_point', response.data.address.reference_point);
            
            setErro(''); // Limpar qualquer erro anterior
        } catch (error) {
            setErro('Erro ao buscar usuários'); // Definir mensagem de erro
        } finally {
        }
    };

    buscarTodosUsuarios();
}, [GetCliente]);


  const onSubmit = (data: IContactFormProps) => {
    data.address.id = 1;
    AtualizarCliente(Number(clienteId),String(data.client_first_name), String(data.client_last_name),String(data.cpf), String(data.phone_number),String(data.email),(data.address) )    
    
    if(!EditarClienteStatus){
        setTimeout(() => {
          // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
          alert("A página será recarregada agora.");
        
          // Recarregar a página
          navigate("/verifyUser/dashboardcliente");
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

const estadosBrasileiros = [
    { sigla: "AC", nome: "Acre" },
    { sigla: "AL", nome: "Alagoas" },
    // Adicione todos os estados...
    { sigla: "SP", nome: "São Paulo" },
    { sigla: "SE", nome: "Sergipe" },
    { sigla: "TO", nome: "Tocantins" }
  ];

  return (
    <div className="background-container">
        <div  className='container_form'>
                <h1 className='loginTxt'>Editar Cliente</h1>
                <form className='Form' onSubmit={handleSubmit(onSubmit)} >
                    <div className="form-row">
                        <div className="form-column">

                            <div className='containerInput'>
                                <AiOutlineMail  style={{color:"gray"}} className='icon' size={24}/>
                                <input  className='inputC' type="text" placeholder=' Primeiro nome' {...register('client_first_name')}  />
                            </div>
                            {errors.client_first_name && <span className='errorSpan01'>Preencha todos os campos</span>}

                            <div className='containerInput'>
                                <AiOutlineMail  style={{color:"gray"}} className='icon' size={24}/>
                                <input  className='inputC' type="text" placeholder=' Ultimo nome' {...register('client_last_name')}  />
                            </div>
                            {errors.client_last_name && <span className='errorSpan01'>Preencha todos os campos</span>}

                            <div className='containerInput'>
                                <AiOutlineMail  style={{color:"gray"}} className='icon' size={24}/>
                                <input  className='inputC' type="email" placeholder=' Email' {...register('email')}  />
                            </div>
                            {errors.email && <span className='errorSpan01'>Preencha todos os campos</span>}

                            <div className='containerInput'>
                                <AiOutlineKey  style={{color:"gray"}} className='icon' size={24}/>
                                <input  className='inputC' type="number" placeholder=' CPF' {...register('cpf')} />
                            </div>
                            {errors.cpf && <span className='errorSpan01'>Preencha todos os campos</span>}

                            <div className='containerInput'>
                                <AiOutlinePhone  style={{color:"gray"}} className='icon' size={24}/>
                                <input  className='inputC' type="number" placeholder='  phone_number' {...register('phone_number')}/>
                            </div>
                            {errors. phone_number && <span className='errorSpan01'>Preencha todos os campos</span>}

                            <div className='containerInput'>
                                <input className='inputC' type="text" placeholder='Tipo' {...register('address.type')} />
                            </div>
                            {errors.address?.type && <span className='errorSpan01'>Preencha todos os campos</span>}

                        </div>

                        <div className="form-column">
                            <div className='containerInput'>
                                <select className='inputC' {...register('address.state')}>
                                    <option value="">Selecione um estado</option>
                                    {estadosBrasileiros.map((estado) => (
                                        <option key={estado.sigla} value={estado.sigla}>{estado.nome}</option>
                                    ))}
                                </select>
                            </div>
                            {errors.address?.state && <span className='errorSpan01'>{errors.address.state.message}</span>}

                            <div className='containerInput'>
                                <input className='inputC' type="text" placeholder='Endereço' {...register('address.address')} />
                            </div>
                            {errors.address?.address && <span className='errorSpan01'>{errors.address.address.message}</span>}

                           
                            
                            <div className='containerInput'>
                                <input className='inputC' type="text" placeholder='Abreviação' {...register('address.abbreviation')} />
                            </div>
                            {errors.address?.abbreviation && <span className='errorSpan01'>{errors.address.abbreviation.message}</span>}

                            <div className='containerInput'>
                                <input className='inputC' type="text" placeholder='Cidade' {...register('address.city')} />
                            </div>
                            {errors.address?.city && <span className='errorSpan01'>{errors.address.city.message}</span>}

                            <div className='containerInput'>
                                <input className='inputC' type="text" placeholder='Bairro' {...register('address.neighborhood')} />
                            </div>
                            {errors.address?.neighborhood && <span className='errorSpan01'>{errors.address.neighborhood.message}</span>}

                            <div className='containerInput'>
                                <input className='inputC' type="text" placeholder='Ponto de Referência' {...register('address.reference_point')} />
                            </div>
                            {errors.address?.reference_point && <span className='errorSpan01'>{errors.address.reference_point.message}</span>}
                        </div>
                            

                        


                    </div>
                    <div className='Container_button'>
                            <ButtomCustom />
                    </div>

                </form>
            
        </div>
    </div>
  )
}

