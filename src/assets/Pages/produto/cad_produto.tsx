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
    descricao?: string;
    unidade_idunidade?: number;
    valor_compra?:number;
    valor_venda?:number;
    quantidade:number;
}
const contactSchema= yup.object().shape({
    descricao: yup.string().required(),
    unidade_idunidade: yup.number().required(),
    valor_compra:yup.number().required(),
    valor_venda:yup.number().required(),
    quantidade:yup.number().required(),
});


export const Cadastro_Produto:React.FC = () => {
	const {RegistrarProduto,cadastroProdutoStatus} = useAuth()
  const { register, handleSubmit, formState } = useForm({
    reValidateMode: 'onBlur',
    resolver: yupResolver(contactSchema),
  });
  const navigate = useNavigate();
  const { errors } = formState;

  const onSubmit = (data: IContactFormProps) => {
    RegistrarProduto(String(data.descricao), Number(data.unidade_idunidade),Number(data.valor_compra), Number(data.valor_venda),Number(data.quantidade))
  
    if(!cadastroProdutoStatus){
        setTimeout(() => {
          // Aqui você pode colocar qualquer lógica que queira executar antes do recarregamento
          alert("A página será recarregada agora.");
        
          // Recarregar a página
          navigate("/verifyUser/dashboardproduto");
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
            <h1 className='loginTxt'>Cadastrar Produto</h1>
            <form className='Form' onSubmit={handleSubmit(onSubmit)} >

                <div className='containerInput'>
                    <AiTwotoneSchedule  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="text" placeholder=' Descrição' {...register('descricao')}/>
                </div>
                {errors.descricao && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlineNumber   style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='Quantidade' {...register('quantidade')}/>
                </div>
                {errors.quantidade && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlineShoppingCart   style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='Valor da compra' {...register('valor_compra')}  />
                </div>
                {errors.valor_compra && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <AiOutlineFund  style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder=' Valor da venda' {...register('valor_venda')} />
                </div>
                {errors.valor_venda && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='containerInput'>
                    <FaBarcode   style={{color:"gray"}} className='icon' size={24}/>
                    <input  className='inputC' type="number" placeholder='ID Unidade' {...register('unidade_idunidade')}/>
                </div>
                {errors.unidade_idunidade && <span className='errorSpan01'>Preencha todos os campos</span>}

                <div className='Container_button'>
                    <ButtomCustom />
                </div>
            </form>
        </div>
  </div>
  )
}
