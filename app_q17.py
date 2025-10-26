import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from q17_bookstore_simulation import run_bookstore_simulation

st.set_page_config(page_title="Q17: Bookstore Inventory Simulation", layout="wide")

st.title("Question 17: Bookstore Inventory Simulation")
st.markdown("### Monte Carlo Simulation for Book Inventory Management")

st.markdown("""
**Problem:**
- Book cost: $15, Selling price: $25, Return value: $5
- Profit per book sold: $10
- Loss per unsold book: $10 (cost $15 - return $5)
- Lost profit from excess demand: $10 per book
""")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")

stock_quantity = st.sidebar.number_input(
    "Books to stock each day", 
    min_value=50, 
    max_value=110, 
    value=90, 
    step=10,
    help="Must be in multiples of 10"
)

num_days = st.sidebar.number_input(
    "Number of days to simulate", 
    min_value=1, 
    max_value=365, 
    value=20, 
    step=1
)

random_seed = st.sidebar.number_input(
    "Random seed (for reproducibility)", 
    min_value=0, 
    max_value=99999, 
    value=42, 
    step=1
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Financial Parameters:**")
st.sidebar.info("""
- Cost per book: $15
- Selling price: $25
- Return value: $5
- Profit per sale: $10
- Loss per unsold: $10
- Lost profit/book: $10
""")

# Display demand distribution
st.header("Demand Distribution")
st.markdown("**Day Type Probabilities:**")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("High Demand", "0.4", help="100 books sold")
with col2:
    st.metric("Medium Demand", "0.3", help="80 books sold")
with col3:
    st.metric("Low Demand", "0.3", help="50 books sold")

st.markdown("**Distribution of books demanded on each type of day:**")

# Create distribution table
distribution_data = {
    'Demand': [50, 60, 70, 80, 90, 100, 110],
    'High (P=0.4)': [0.05, 0.07, 0.1, 0.2, 0.3, 0.15, 0.13],
    'Medium (P=0.3)': [0.12, 0.16, 0.3, 0.2, 0.08, 0.06, 0.08],
    'Low (P=0.3)': [0.3, 0.2, 0.06, 0.12, 0.13, 0.09, 0.1]
}
df_distribution = pd.DataFrame(distribution_data)
st.dataframe(df_distribution, use_container_width=True)

# Run simulation button
st.markdown("---")
if st.button("Run Simulation", type="primary"):
    st.header("Simulation Results")
    
    with st.spinner("Running simulation..."):
        results = run_bookstore_simulation(stock_quantity, num_days, random_seed)
    
    # Display summary statistics
    st.subheader("Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Days", results['num_days'])
    with col2:
        st.metric("Books Stocked/Day", results['stock_quantity'])
    with col3:
        st.metric("Total Profit", f"${results['total_profit']:,.2f}")
    with col4:
        st.metric("Avg Profit/Day", f"${results['avg_profit_per_day']:,.2f}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Demand", f"{results['avg_demand']:.2f}")
    with col2:
        st.metric("Avg Books Sold", f"{results['avg_sold']:.2f}")
    with col3:
        st.metric("Avg Unsold", f"{results['avg_unsold']:.2f}")
    with col4:
        st.metric("Avg Lost Sales", f"{results['avg_lost_sales']:.2f}")
    
    # Day type analysis
    st.markdown("---")
    st.subheader("Analysis by Day Type")
    
    day_type_stats = {}
    for day_type in ['High', 'Medium', 'Low']:
        day_data = [d for d in results['daily_results'] if d['day_type'] == day_type]
        if day_data:
            day_type_stats[day_type] = {
                'Count': len(day_data),
                'Avg Demand': np.mean([d['demand'] for d in day_data]),
                'Avg Sold': np.mean([d['sold'] for d in day_data]),
                'Avg Unsold': np.mean([d['unsold'] for d in day_data]),
                'Avg Lost Sales': np.mean([d['lost_sales'] for d in day_data]),
                'Avg Profit': np.mean([d['profit'] for d in day_data]),
                'Total Profit': np.sum([d['profit'] for d in day_data])
            }
    
    df_day_type = pd.DataFrame(day_type_stats).T
    df_day_type = df_day_type.round(2)
    st.dataframe(df_day_type, use_container_width=True)
    
    # Profit distribution
    st.markdown("---")
    st.subheader("Profit Analysis")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Histogram of daily profits
    profits = [d['profit'] for d in results['daily_results']]
    ax1.hist(profits, bins=20, edgecolor='black', alpha=0.7, color='#2ca02c')
    ax1.set_xlabel('Daily Profit ($)', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title('Distribution of Daily Profits', fontsize=12, fontweight='bold')
    ax1.axvline(results['avg_profit_per_day'], color='red', linestyle='--', linewidth=2,
                label=f'Mean: ${results["avg_profit_per_day"]:.2f}')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Cumulative profit over time
    cumulative_profit = np.cumsum(profits)
    days = range(1, num_days + 1)
    ax2.plot(days, cumulative_profit, linewidth=2, color='#1f77b4')
    ax2.set_xlabel('Day', fontsize=11)
    ax2.set_ylabel('Cumulative Profit ($)', fontsize=11)
    ax2.set_title('Cumulative Profit Over Time', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    # Display daily results
    st.markdown("---")
    st.subheader("Daily Breakdown")
    
    df_daily = pd.DataFrame(results['daily_results'])
    df_daily['Day'] = df_daily['day']
    df_daily['Day Type'] = df_daily['day_type']
    df_daily['Demand'] = df_daily['demand']
    df_daily['Sold'] = df_daily['sold']
    df_daily['Unsold'] = df_daily['unsold']
    df_daily['Lost Sales'] = df_daily['lost_sales']
    df_daily['Revenue'] = df_daily['revenue'].apply(lambda x: f"${x:.2f}")
    df_daily['Cost'] = df_daily['cost'].apply(lambda x: f"${x:.2f}")
    df_daily['Return'] = df_daily['return_value'].apply(lambda x: f"${x:.2f}")
    df_daily['Lost Profit'] = df_daily['lost_profit'].apply(lambda x: f"${x:.2f}")
    df_daily['Daily Profit'] = df_daily['profit'].apply(lambda x: f"${x:.2f}")
    
    display_df = df_daily[['Day', 'Day Type', 'Demand', 'Sold', 'Unsold', 
                            'Lost Sales', 'Revenue', 'Cost', 'Return', 
                            'Lost Profit', 'Daily Profit']]
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download button for results
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="Download Daily Results as CSV",
        data=csv,
        file_name=f"bookstore_simulation_{num_days}days_{stock_quantity}stock.csv",
        mime="text/csv"
    )

# Instructions
with st.expander("ℹ️ How to use this tool"):
    st.markdown("""
    1. **Set Parameters** in the sidebar:
       - **Books to stock**: Number of books to stock each day (must be multiple of 10)
       - **Number of days**: How many days to simulate
       - **Random seed**: For reproducible results
    
    2. **Understanding the simulation**:
       - Each day is randomly assigned a demand type (High/Medium/Low)
       - Demand quantity is randomly selected from the distribution for that day type
       - Profit is calculated based on books sold, unsold, and lost sales
    
    3. **Financial Calculations**:
       - Revenue = Books sold × $25
       - Cost = Books stocked × $15
       - Return = Unsold books × $5
       - Lost Profit = Lost sales × $10
       - Daily Profit = Revenue - Cost + Return - Lost Profit
    
    4. **Interpreting Results**:
       - View summary statistics for overall performance
       - Analyze by day type to understand different demand scenarios
       - Check daily breakdown for detailed day-by-day results
       - Download CSV for further analysis
    """)

with st.expander("📊 Problem Details"):
    st.markdown("""
    **Given Information:**
    - Book cost: $15
    - Book selling price: $25
    - Return value for unsold books: $5
    - Lost profit from stockout: $10 per book
    
    **Demand Scenarios:**
    - High demand (P=0.4): Typically 100 books
    - Medium demand (P=0.3): Typically 80 books
    - Low demand (P=0.3): Typically 50 books
    
    **Constraint:**
    - Books can only be stocked in multiples of 10
    
    **Objective:**
    - Simulate total profit for 20 days if the bookstore owner stocks 90 books each day
    """)