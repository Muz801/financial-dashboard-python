import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

IVA = 0.13

# -------------------------
# 📥 CARGAR DATOS
# -------------------------
df = pd.read_csv("data/transactions_full.csv")
df["fecha"] = pd.to_datetime(df["fecha"])

# -------------------------
# 💰 CALCULOS
# -------------------------
ventas = df[df["cuenta"] == "Ventas"]["monto"].sum()
compras = df[df["cuenta"] == "Compras"]["monto"].sum()
utilidad_bruta = ventas - compras

gastos = df[
    (df["tipo"] == "gasto") &
    (df["cuenta"] != "Compras")
]["monto"].sum()

iva = (ventas * IVA) - (compras * IVA)
utilidad_neta = utilidad_bruta - gastos - iva

# -------------------------
# 🖥️ UI
# -------------------------
st.title("📊 Dashboard Financiero")

st.metric("💰 Ventas", f"₡{ventas:,.0f}")
st.metric("💸 Gastos", f"₡{gastos:,.0f}")
st.metric("📈 Utilidad Neta", f"₡{utilidad_neta:,.0f}")

# -------------------------
# 📊 GRAFICO GASTOS
# -------------------------
st.subheader("📊 Gastos por categoría")

gastos_categoria = df[
    (df["tipo"] == "gasto") &
    (df["cuenta"] != "Compras")
].groupby("cuenta")["monto"].sum()

fig, ax = plt.subplots()
gastos_categoria.plot(kind="bar", ax=ax)
st.pyplot(fig)

# -------------------------
# 📋 TABLA
# -------------------------
st.subheader("📋 Datos")
st.dataframe(df)