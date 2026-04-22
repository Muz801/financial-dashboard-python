import pandas as pd
import smtplib
from email.message import EmailMessage
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------
# 📧 CONFIGURACIÓN
# -------------------------
EMAIL = "pablomail8001@gmail.com"
APP_PASSWORD = "eaxwatjadvqzjihs"

recipients = [
    "sjzo0600@gmail.com",
    "pablojoel00@hotmail.com",
    "ofeliapada@gmail.com"
]

IVA = 0.13

# -------------------------
# 📥 CARGAR DATOS
# -------------------------
df = pd.read_csv("../data/transactions_full.csv")

# -------------------------
# 💰 CÁLCULOS
# -------------------------
ventas = df[df["cuenta"] == "Ventas"]["monto"].sum()
compras = df[df["cuenta"] == "Compras"]["monto"].sum()

utilidad_bruta = ventas - compras

gastos = df[
    (df["tipo"] == "gasto") &
    (df["cuenta"] != "Compras")
]["monto"].sum()

iva_ventas = ventas * IVA
iva_compras = compras * IVA
iva_pagar = iva_ventas - iva_compras

utilidad_neta = utilidad_bruta - gastos - iva_pagar

# -------------------------
# 📄 CREAR PDF
# -------------------------
pdf_path = "../data/reporte_financiero.pdf"

doc = SimpleDocTemplate(pdf_path)
styles = getSampleStyleSheet()

contenido = []

contenido.append(Paragraph("📊 REPORTE FINANCIERO - ENERO 2026", styles["Title"]))
contenido.append(Spacer(1, 10))

contenido.append(Paragraph(f"Ventas: ₡{ventas:,.0f}", styles["Normal"]))
contenido.append(Paragraph(f"Compras: ₡{compras:,.0f}", styles["Normal"]))
contenido.append(Paragraph(f"Utilidad Bruta: ₡{utilidad_bruta:,.0f}", styles["Normal"]))
contenido.append(Spacer(1, 10))

contenido.append(Paragraph(f"Gastos Operativos: ₡{gastos:,.0f}", styles["Normal"]))
contenido.append(Spacer(1, 10))

contenido.append(Paragraph(f"IVA Ventas: ₡{iva_ventas:,.0f}", styles["Normal"]))
contenido.append(Paragraph(f"IVA Compras: ₡{iva_compras:,.0f}", styles["Normal"]))
contenido.append(Paragraph(f"IVA a pagar: ₡{iva_pagar:,.0f}", styles["Normal"]))
contenido.append(Spacer(1, 10))

contenido.append(Paragraph(f"Utilidad Neta: ₡{utilidad_neta:,.0f}", styles["Normal"]))

doc.build(contenido)

print("📄 PDF generado")

# -------------------------
# 📧 BODY DEL CORREO
# -------------------------
body = f"""
📊 REPORTE FINANCIERO - ENERO 2026

💰 Ventas: ₡{ventas:,.0f}
📦 Compras: ₡{compras:,.0f}

📊 Utilidad Bruta: ₡{utilidad_bruta:,.0f}

💸 Gastos: ₡{gastos:,.0f}

🧾 IVA a pagar: ₡{iva_pagar:,.0f}

📈 Utilidad Neta: ₡{utilidad_neta:,.0f}
"""

# -------------------------
# 📧 ENVIAR CORREOS (PRO)
# -------------------------
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, APP_PASSWORD)

    for recipient in recipients:

        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = recipient
        msg["Subject"] = "📊 Reporte Financiero Enero"

        msg.set_content(body)

        # 📎 PDF
        with open(pdf_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename="reporte_financiero.pdf"
            )

        # 📎 CSV (DATA ORIGINAL)
        with open("../data/transactions_full.csv", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="csv",
                filename="transactions_january.csv"
            )

        smtp.send_message(msg)

        print(f"📧 Correo enviado a {recipient}")