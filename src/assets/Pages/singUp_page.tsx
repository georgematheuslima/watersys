import { useForm } from 'react-hook-form';
import * as yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';


type FormData = {
    nomeCompleto: string;
    cpf: string;
    endereco: string;
    contato: string;
  };
  

const schema = yup.object().shape({
  nomeCompleto: yup.string().required('Nome completo é obrigatório'),
  cpf: yup
    .string()
    .matches(/^\d{3}\.\d{3}\.\d{3}-\d{2}$/, 'CPF inválido')
    .required('CPF é obrigatório'),
  endereco: yup.string().required('Endereço é obrigatório'),
  contato: yup.string().required('Contato é obrigatório'),
});


export const SingUp_page:React.FC = () => {
    const { handleSubmit, register, formState: { errors } } = useForm<FormData>({
        resolver: yupResolver(schema),
      });
    
      const onSubmit = (data: FormData) => {
        console.log(data);
      };
    
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label>Nome Completo:</label>
        <input {...register("nomeCompleto")} />
        {errors.nomeCompleto && <p>{errors.nomeCompleto.message}</p>}
      </div>
      <div>
        <label>CPF:</label>
        <input {...register("cpf")} />
        {errors.cpf && <p>{errors.cpf.message}</p>}
      </div>
      <div>
        <label>Endereço:</label>
        <input {...register("endereco")} />
        {errors.endereco && <p>{errors.endereco.message}</p>}
      </div>
      <div>
        <label>Contato:</label>
        <input {...register("contato")} />
        {errors.contato && <p>{errors.contato.message}</p>}
      </div>
      <button type="submit">Enviar</button>
    </form>
  )
}
