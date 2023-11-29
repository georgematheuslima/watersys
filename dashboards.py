import logging

import streamlit as st
import requests
import plotly.express as px
from datetime import datetime

LOGGER = logging.getLogger('sLogger')

def main():
    st.title('Integração Streamlit e FastAPI')
    
    st.write("Este é um aplicativo Streamlit integrado a uma API FastAPI do sistema Watersys!")

    @st.cache_data
    def get_data():
        try:    
            response = requests.get('http://app:8000/api/v1/sales/sales')
            LOGGER.info(response.content)
            if response.text:
                return response.json()
            else:
                st.error(f"Erro ao buscar dados. Status Code: {response.status_code}")
        except requests.RequestException as e:
            st.error(f"Erro de conexão: {e}")

    def extract_unique_months(data):
        unique_months = set()
        for item in data:
            date_obj = datetime.strptime(item['purchase_date'], '%Y-%m-%d')
            unique_months.add(date_obj.strftime('%B %Y'))

        # Mapeamento de nomes de meses para números
        months_mapping = {
            'January': 0,
            'February': 1,
            'March': 2,
            'April': 3,
            'May': 4,
            'June': 5,
            'July': 6,
            'August': 7,
            'September': 8,
            'October': 9
        }

        # Ordene os meses usando o mapeamento
        unique_months_sorted = sorted(unique_months, 
                                    key=lambda x: (datetime.strptime(x, '%B %Y').year, months_mapping[x.split()[0]]))

        return unique_months_sorted

    def filter_data_by_month(data, selected_month):
        filtered_data = [item for item in data if datetime.strptime(item['purchase_date'], '%Y-%m-%d').strftime('%B %Y') == selected_month]
        return filtered_data

    def filter_total_amount_by_month(data, selected_month):
        filtered_total_amount = [item['total_amount'] for item in data if datetime.strptime(item['purchase_date'], '%Y-%m-%d').strftime('%B %Y') == selected_month]
        return filtered_total_amount

    def extract_days_from_dates(data):
        days_list = [datetime.strptime(item['purchase_date'], '%Y-%m-%d').day for item in data]
        return days_list

    data = get_data()
    if data:
        st.write("Dados da API FastAPI:")

        unique_months = extract_unique_months(data)
        selected_month = st.sidebar.selectbox("Selecione um mês:", unique_months)
        
        filtered_data = filter_data_by_month(data, selected_month)
        
        if filtered_data:
            # Exibição dos dados filtrados em uma tabela
            st.write(f"Compras para o mês de {selected_month}:")
            st.table(filtered_data)

            # Gráfico de faturamento por dia do mês
            days = extract_days_from_dates(filtered_data)
            total_amount_by_day = filter_total_amount_by_month(filtered_data, selected_month)
            fig_date = px.bar(x=days, y=total_amount_by_day, labels={'x': 'Dia do Mês', 'y': 'Faturamento'}, title="Faturamento por dia do mês")
            st.plotly_chart(fig_date)

            # 1. Dia com a maior quantidade de compras
            day_max_purchases = days[total_amount_by_day.index(max(total_amount_by_day))]
            st.write(f"Dia com maior quantidade de compras: {day_max_purchases}")

            # 2. Total do mês vs total acumulado até o momento
            total_current_month = sum(total_amount_by_day)
            total_until_now = sum(filter_total_amount_by_month(data, selected_month))  # Total até o momento
            fig_totals = px.bar(x=['Total do Mês', 'Total até o Momento'], y=[total_current_month, total_until_now], labels={'x': 'Total', 'y': 'Faturamento'}, title="Comparação de Totais")
            st.plotly_chart(fig_totals)

            # 3. Mês com mais vendas vs total acumulado até o momento
            months_sales = {month: sum(filter_total_amount_by_month(data, month)) for month in unique_months}
            max_sales_month = max(months_sales, key=months_sales.get)
            max_sales_value = months_sales[max_sales_month]
            st.write(f"Mês com mais vendas: {max_sales_month} (Total: {max_sales_value})")
            
            fig_monthly_sales = px.bar(x=list(months_sales.keys()), y=list(months_sales.values()), labels={'x': 'Mês', 'y': 'Faturamento'}, title="Faturamento por Mês")
            st.plotly_chart(fig_monthly_sales)

        else:
            st.write("Nenhuma compra encontrada para este mês.")
if __name__ == '__main__':
    main()

