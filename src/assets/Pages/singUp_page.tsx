import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';


type FormData = {
     nameCompleto: string;
    cpf: string;
    endereco: string;
     phone_number: string;
  };
  

const schema = yup.object().shape({
   nameCompleto: yup.string().required(' name completo é obrigatório'),
  cpf: yup
    .string()
    .matches(/^\d{3}\.\d{3}\.\d{3}-\d{2}$/, 'CPF inválido')
    .required('CPF é obrigatório'),
  endereco: yup.string().required('Endereço é obrigatório'),
   phone_number: yup.string().required(' phone_number é obrigatório'),
});


export const SingUp_page:React.FC = () => {
    const { handleSubmit, register, formState: { errors } } = useForm<FormData>({
        resolver: yupResolver(schema),
      });
    
      const onSubmit = (data: FormData) => {
        console.log(data);
      };
    
  return (
    <div className="background-container">
    <form  className='Form' onSubmit={handleSubmit(onSubmit)}>
      <div className='containerInput'>
        <label> name Completo:</label>
        <input className='inputC' {...register("nameCompleto")} />
        {errors. nameCompleto && <p>{errors. nameCompleto.message}</p>}
      </div>
      <div className='containerInput'>
        <label>CPF:</label>
        <input {...register("cpf")} />
        {errors.cpf && <p>{errors.cpf.message}</p>}
      </div>
      <div className='containerInput'>
        <label>Endereço:</label>
        <input {...register("endereco")} />
        {errors.endereco && <p>{errors.endereco.message}</p>}
      </div>
      <div className='containerInput'>
        <label> phone_number:</label>
        <input {...register("phone_number")} />
        {errors. phone_number && <p>{errors. phone_number.message}</p>}
      </div>
      <button  className='Container_button' type="submit">Enviar</button>
    </form>
    </div>
  )
}
