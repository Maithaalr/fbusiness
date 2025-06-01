import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import BytesIO

# --- Setup ---
st.set_page_config(page_title="Business Dashboard", layout="centered")

st.title("Future Business Center")


# --- Tabs ---
tab1, tab2 = st.tabs([" Calculator", " Business Insights"])

with tab1:
    st.title(" Revenue and Expenses")

    # Revenue Input
    st.subheader(" Revenue Items")
    revenue_data = []
    num_revenue = st.number_input("How many revenue items?", min_value=1, max_value=10, step=1)
    for i in range(num_revenue):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"Revenue Item {i+1}", key=f"rev_name_{i}")
        with col2:
            amount = st.number_input("Amount (AED)", key=f"rev_amt_{i}", min_value=0.0, step=100.0)
        revenue_data.append({"Item": name, "Amount": amount})
    revenue_df = pd.DataFrame(revenue_data)
    total_revenue = revenue_df["Amount"].sum()

    # Expense Input
    st.subheader(" Expense Items")
    expense_data = []
    num_expense = st.number_input("How many expense items?", min_value=1, max_value=10, step=1)
    for i in range(num_expense):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"Expense Item {i+1}", key=f"exp_name_{i}")
        with col2:
            amount = st.number_input("Amount (AED)", key=f"exp_amt_{i}", min_value=0.0, step=100.0)
        expense_data.append({"Item": name, "Amount": amount})
    expense_df = pd.DataFrame(expense_data)
    total_expenses = expense_df["Amount"].sum()

    # Calculations
    profit = total_revenue - total_expenses
    profit_percent = (profit / total_revenue * 100) if total_revenue > 0 else 0

    # Summary
    st.subheader(" Summary")
    st.write(f"**Total Revenue:** AED {total_revenue:,.2f}")
    st.write(f"**Total Expenses:** AED {total_expenses:,.2f}")
    if profit >= 0:
        st.success(f" Profit: AED {profit:,.2f} ({profit_percent:.2f}%)")
    else:
        st.error(f" Loss: AED {abs(profit):,.2f} ({abs(profit_percent):.2f}%)")

    # Plotly Chart
    st.subheader(" Revenue vs Expenses vs Profit")
    fig = go.Figure(data=[
        go.Bar(name="Revenue", x=["Revenue"], y=[total_revenue], marker_color="rgb(93, 173, 226)",
               text=[f"AED {total_revenue:,.2f}"], textposition="auto",
               hovertemplate='Revenue: %{y:.2f} AED'),
        go.Bar(name="Expenses", x=["Expenses"], y=[total_expenses], marker_color="rgb(52, 152, 219)",
               text=[f"AED {total_expenses:,.2f}"], textposition="auto",
               hovertemplate='Expenses: %{y:.2f} AED'),
        go.Bar(name="Profit", x=["Profit"], y=[profit], marker_color="rgb(40, 116, 166)",
               text=[f"AED {profit:,.2f}"], textposition="auto",
               hovertemplate='Profit: %{y:.2f} AED')
    ])
    fig.update_layout(barmode='group', yaxis_title="Amount (AED)")
    st.plotly_chart(fig, use_container_width=True)

    # Excel Export
    st.subheader(" Download Excel")
    if st.button("Download All Data as Excel"):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            revenue_df.to_excel(writer, index=False, sheet_name="Revenue")
            expense_df.to_excel(writer, index=False, sheet_name="Expenses")
        st.download_button(" Click to Download", output.getvalue(), file_name="business_data.xlsx")

with tab2:
    st.title(" Business Insights")
    if not revenue_df.empty and not expense_df.empty:
        max_rev = revenue_df.loc[revenue_df["Amount"].idxmax()]
        max_exp = expense_df.loc[expense_df["Amount"].idxmax()]
        st.write(f" Highest Revenue Item: **{max_rev['Item']}** — AED {max_rev['Amount']:,.2f}")
        st.write(f" Highest Expense Item: **{max_exp['Item']}** — AED {max_exp['Amount']:,.2f}")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(revenue_df.sort_values(by="Amount", ascending=False).reset_index(drop=True), use_container_width=True)
        with col2:
            st.dataframe(expense_df.sort_values(by="Amount", ascending=False).reset_index(drop=True), use_container_width=True)
    else:
        st.warning("Please enter data in the Dashboard tab first.")
