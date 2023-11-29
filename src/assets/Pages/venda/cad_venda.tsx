import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { AiOutlineNumber ,AiOutlineShoppingCart, AiTwotoneSchedule, AiOutlineFund } from "react-icons/ai";
import"../../scss/Login_Page.scss"
import * as yup from 'yup';
import React from 'react';
import { useAuth } from '../../../context/AuthProvider/AuthContext';
import { FaBarcode } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

type IContactFormProps = {
    quantity?: number;
    returnable?: boolean;
    product_id?:number;
    cpf?:string;
}
const contactSchema= yup.object().shape({
    quantity: yup.number().required(),
    returnable: yup.boolean().required(),
    product_id:yup.number().required(),
    cpf:yup.string().required(),
});


export const Registra_Vendas:React.FC = () => {
	const {RegistrarVenda,registarVendaStatus} = useAuth()
  const { register, handleSubmit, formState } = useForm({
    reValidateMode: 'onBlur',
    resolver: yupResolver(contactSchema),
  });
  const navigate = useNavigate();
  const { errors } = formState;

  const onSubmit = (data: IContactFormProps) => {
    RegistrarVenda(Number(data.quantity), Boolean(data.returnable),Number(data.product_id), String(data.cpf))
   
    if(!registarVendaStatus){
        setTimeout(() => {
          // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
          alert("A página será recarregada agora.");
        
          // Recarregar a página
          navigate("/verifyUser/dashboardVendas");
        }, 2000);
    }else{
        setTimeout(() => {
            alert("Venda não registrada");
        }, 1000);
    }
};
  
const ButtomCustom = () =>{
  return(
    <div>
      <button style={{backgroundColor:"#1b8cba"}} type="submit" className="login-button-submit">Confirmar Venda</button>
    </div>
  )
}
  return (
    <div className="background-container">
        <div  className='container_form'>
            <h1 className='loginTxt'>Tela de Venda</h1>
            <form className='Form' onSubmit={handleSubmit(onSubmit)} >

                <div className='containerInput'>
                    <AiTwotoneSchedule  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder=' Quantidade' {...register('quantity')}/>
                </div>
                {errors.quantity && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlineNumber   style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='ID Produto' {...register('product_id')}/>
                </div>
                {errors.product_id && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiTwotoneSchedule   style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='CPF' {...register('cpf')}  />
                </div>
                {errors.cpf && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerCheckbox '>
                    <input type="checkbox" id="is_admin" className="checkboxStyle" {...register('returnable')}/>
                    <label htmlFor="returnable">Retornavel</label>
                </div>
                {errors.returnable && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='Container_button'>
                    <ButtomCustom />
                </div>
            </form>
        </div>
  </div>
  )
}
