import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate cash flow
def calculate_cash_flow(months, savings, sales):
    data = []
    cumulative_cash_flow = 0
    for month in range(1, months + 1):
        consulting_cost = 4500 if month == 1 else (10500 if month == 3 else 0)
        licensing_cost = 0.765 if month <= 3 else (1.530 if month <= 6 else 2.295)
        cloud_cost = 0.511 if month <= 3 else (0.414 if month <= 6 else 0.746)
        total_cost = consulting_cost + licensing_cost + cloud_cost
        total_revenue = savings + sales if month >= 3 else 0
        cash_flow = total_revenue - total_cost
        cumulative_cash_flow += cash_flow
        data.append([month, consulting_cost, licensing_cost, cloud_cost, total_cost, total_revenue, cash_flow, cumulative_cash_flow])
    return pd.DataFrame(data, columns=["Periodo", "Costo de Consultoría", "Costo de Licenciamiento", "Costo de Alojamiento", "Costo Total", "Ingresos Totales", "Flujo de Caja", "Flujo de Caja Acumulado"])

# Streamlit UI
st.title("Flujo de Caja Interactivo")

# Parameters
st.sidebar.header("Parámetros")
months = st.sidebar.slider("Número de Periodos", 1, 12, 8)
savings = st.sidebar.number_input("Ahorros por Periodo ($)", value=95.74)
sales = st.sidebar.number_input("Ingresos por Periodo por ventas ($)", value=0)

# Calculate Cash Flow
df = calculate_cash_flow(months, savings, sales)

# Display Data
st.header("Datos de Flujo de Caja")
st.dataframe(df)

# Visualize Cash Flow
st.header("Gráfico de Flujo de Caja")
fig, ax = plt.subplots()
ax.plot(df["Periodo"], df["Flujo de Caja Acumulado"], label="Flujo de Caja Acumulado", marker="o")
ax.plot(df["Periodo"], df["Ingresos Totales"], label="Ingresos Totales", linestyle="--")
ax.plot(df["Periodo"], df["Costo Total"], label="Costo Total", linestyle="--")
ax.set_xlabel("Periodo")
ax.set_ylabel("Cantidad ($)")
ax.set_title("Análisis de Flujo de Caja")
ax.legend()
st.pyplot(fig)

# Save user interactions
if st.button("Save Data"):
    df.to_csv("user_interactions.csv", index=False)
    st.success("User interactions saved!")
