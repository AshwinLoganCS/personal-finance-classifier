"""
Personal Finance Expense Classifier - Streamlit Application
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

from classifier import get_classifier, get_all_categories
from utils import (
    clean_csv_data,
    add_derived_columns,
    validate_csv_structure,
    extract_merchant_name,
    smart_read_csv,
    detect_header_row,
    normalize_column_names
)


# Page configuration
st.set_page_config(
    page_title="Personal Finance Expense Classifier",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application function."""
    
    # Title and description
    st.title("💰 Personal Finance Expense Classifier")
    st.markdown("""
    Upload your bank statement CSV to automatically categorize transactions, 
    visualize spending patterns, and gain insights into your financial habits.
    """)
    
    # Sidebar for upload and settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=['csv'],
            help="CSV should contain columns: date, description, amount"
        )
        
        st.markdown("---")
        
        # Advanced options - Make more prominent for bank CSVs
        st.subheader("🔧 CSV Format Options")
        
        auto_detect = st.checkbox(
            "Auto-detect header row",
            value=True,
            help="Automatically find the row containing 'date', 'description', 'amount'"
        )
        
        skip_rows = st.number_input(
            "Manual: Skip rows from top",
            min_value=0,
            max_value=20,
            value=0,
            help="If your CSV has summary rows at the top, specify how many rows to skip. Most bank statements need 5-7 rows skipped.",
            disabled=auto_detect
        )
        
        if not auto_detect:
            st.info("💡 Tip: Most bank CSVs have 5-7 summary rows before the transaction data starts.")
        
        st.markdown("---")
        
        # Classifier selection
        classifier_type = st.radio(
            "Classifier Type",
            options=['rule-based', 'ml'],
            index=0,
            help="Rule-based uses keyword matching. ML is for future implementation."
        )
        
        if classifier_type == 'ml':
            st.warning("⚠️ ML classifier is not yet trained. Using rule-based classifier.")
            classifier_type = 'rule-based'
        
        st.markdown("---")
        
        # Instructions
        st.subheader("📋 Instructions")
        st.markdown("""
        1. **Prepare your CSV** with columns:
           - `date`: Transaction date
           - `description`: Transaction description
           - `amount`: Transaction amount
        2. **Upload** the CSV file
        3. **Review** categorized transactions
        4. **Download** the classified data
        
        **Note:** 
        - Negative amounts = Expenses
        - Positive amounts = Income
        """)
    
    # Main content area
    if uploaded_file is None:
        show_landing_page()
    else:
        # Get skip_rows and auto_detect from session state or defaults
        skip_rows_value = st.session_state.get('skip_rows', 0)
        auto_detect_value = st.session_state.get('auto_detect', True)
        process_uploaded_file(uploaded_file, classifier_type, skip_rows_value, auto_detect_value)


def show_landing_page():
    """Display landing page when no file is uploaded."""
    
    st.info("👆 Please upload a CSV file using the sidebar to get started.")
    
    # Sample data format
    st.subheader("📄 Expected CSV Format")
    
    sample_data = pd.DataFrame({
        'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18'],
        'description': ['Starbucks Coffee', 'Whole Foods Market', 'Shell Gas Station', 'Netflix Subscription'],
        'amount': [-5.75, -87.32, -45.00, -15.99]
    })
    
    st.dataframe(sample_data, use_container_width=True)
    
    # Feature highlights
    st.subheader("✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Visualizations")
        st.write("Interactive charts showing spending by category and over time")
    
    with col2:
        st.markdown("### 🤖 Auto-Classification")
        st.write("Intelligent categorization of transactions into 9 categories")
    
    with col3:
        st.markdown("### 💡 Insights")
        st.write("Key metrics including total spending, income, and top merchants")


def process_uploaded_file(uploaded_file, classifier_type, skip_rows=0, auto_detect=True):
    """Process the uploaded CSV file and display results."""
    
    try:
        # Store settings in session state
        st.session_state['skip_rows'] = skip_rows
        st.session_state['auto_detect'] = auto_detect
        
        # Auto-detect header row if enabled
        if auto_detect:
            detected_skip = detect_header_row(uploaded_file)
            if detected_skip > 0:
                st.info(f"🔍 Auto-detected: Skipping {detected_skip} header row(s)")
                skip_rows = detected_skip
        
        # Read CSV with smart reader
        df = smart_read_csv(uploaded_file, skip_rows=skip_rows)
        
        if df is None:
            st.error("❌ Unable to parse CSV file. Please check the format and try adjusting 'Skip rows' in Advanced Options.")
            st.info("💡 **Tip:** Most bank statements have summary rows at the top. Try setting 'Skip rows' to 5-10.")
            return
        
        # Normalize column names to handle different bank formats
        df = normalize_column_names(df)
        
        # Validate structure
        is_valid, error_msg = validate_csv_structure(df)
        if not is_valid:
            st.error(f"❌ {error_msg}")
            st.info("💡 **Tip:** Your CSV needs columns with date, description, and amount information. We support various column name formats from different banks.")
            
            # Show preview of what was read
            with st.expander("🔍 Preview of CSV (first 10 rows)"):
                st.dataframe(df.head(10))
            
            # Show detected columns
            st.write("**Detected columns:**", ", ".join(df.columns.tolist()))
            return
        
        # Clean data
        with st.spinner("Cleaning data..."):
            df_clean, removed_rows = clean_csv_data(df)
            df_enhanced = add_derived_columns(df_clean)
        
        # Show removed transactions if any
        if removed_rows:
            with st.expander(f"⚠️ {len(removed_rows)} transaction(s) were filtered out during cleaning"):
                st.warning(f"**{len(removed_rows)} transactions were removed** during data cleaning. Review them below:")
                
                removed_df = pd.DataFrame(removed_rows)
                removed_df = removed_df[['date', 'description', 'amount', 'reason']]
                removed_df.index = range(1, len(removed_df) + 1)
                
                st.dataframe(removed_df, use_container_width=True)
                
                st.info("💡 **Note:** Rows are removed only if they have invalid dates or invalid amounts that cannot be parsed.")
        
        # Classify transactions
        with st.spinner("Classifying transactions..."):
            classifier = get_classifier(classifier_type)
            categories = classifier.classify_batch(
                df_enhanced['description'].tolist(),
                df_enhanced['amount'].tolist()
            )
            df_enhanced['category'] = categories
        
        # Store in session state
        st.session_state['df_processed'] = df_enhanced
        
        # Display results
        display_results(df_enhanced)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)


def display_results(df):
    """Display all results including preview, charts, and insights."""
    
    st.success(f"✅ Successfully processed {len(df)} transactions!")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "📈 Visualizations", 
        "💡 Insights", 
        "📥 Download"
    ])
    
    with tab1:
        display_overview(df)
    
    with tab2:
        display_visualizations(df)
    
    with tab3:
        display_insights(df)
    
    with tab4:
        display_download_section(df)


def display_overview(df):
    """Display data overview and preview."""
    
    st.subheader("📋 Transaction Preview")
    
    # Display options
    col1, col2 = st.columns([1, 1])
    with col1:
        max_rows = min(len(df), 500)  # Cap at 500 for performance
        default_rows = min(20, len(df))
        show_rows = st.slider("Number of rows to display", 5, max_rows, default_rows)
    with col2:
        filter_categories = st.multiselect(
            "Filter by categories (select multiple)",
            options=get_all_categories(),
            default=[],
            help="Select one or more categories to filter. Leave empty to show all."
        )
    
    # Filter data
    df_display = df.copy()
    if filter_categories:  # If any categories selected
        df_display = df_display[df_display['category'].isin(filter_categories)]
        st.info(f"📊 Showing {len(df_display)} transactions matching selected categories: {', '.join(filter_categories)}")
    else:
        st.info(f"📊 Showing all {len(df_display)} transactions")
    
    # Display columns
    display_cols = ['date', 'description', 'amount', 'category']
    
    st.dataframe(
        df_display[display_cols].head(show_rows),
        use_container_width=True
    )
    
    # Summary statistics (based on filtered data)
    st.subheader("📊 Quick Statistics" + (" (Filtered)" if filter_categories else ""))
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Transactions", len(df_display))
    
    with col2:
        expenses = df_display[df_display['amount'] < 0]['amount'].sum()
        st.metric("Total Expenses", f"${abs(expenses):,.2f}")
    
    with col3:
        income = df_display[df_display['amount'] > 0]['amount'].sum()
        st.metric("Total Income", f"${income:,.2f}")
    
    with col4:
        net_flow = expenses + income
        st.metric("Net Cash Flow", f"${net_flow:,.2f}")


def display_visualizations(df):
    """Display all visualizations."""
    
    st.subheader("📈 Spending Visualizations")
    
    # Prepare data for expenses only
    df_expenses = df[df['amount'] < 0].copy()
    df_expenses['abs_amount'] = df_expenses['amount'].abs()
    
    if df_expenses.empty:
        st.warning("No expense transactions found to visualize.")
        return
    
    # Category spending summary
    category_spending = df_expenses.groupby('category')['abs_amount'].sum().sort_values(ascending=False)
    
    # Row 1: Pie and Bar charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🥧 Spending by Category (%)")
        fig_pie = px.pie(
            values=category_spending.values,
            names=category_spending.index,
            title="",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Total Spending by Category")
        fig_bar = px.bar(
            x=category_spending.index,
            y=category_spending.values,
            labels={'x': 'Category', 'y': 'Amount ($)', 'color': 'Amount ($)'},
            title="",
            color=category_spending.values,
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Row 2: Cumulative spending over time
    st.markdown("#### 📅 Cumulative Spending Over Time")
    
    # Calculate cumulative spending (expenses only, sorted by date)
    df_expenses_sorted = df_expenses.sort_values('date').copy()
    df_expenses_sorted['cumulative_spending'] = df_expenses_sorted['abs_amount'].cumsum()
    
    fig_cumulative = px.line(
        df_expenses_sorted,
        x='date',
        y='cumulative_spending',
        title="",
        markers=True
    )
    fig_cumulative.update_traces(
        line_color='#e74c3c', 
        line_width=3,
        marker=dict(size=8)
    )
    fig_cumulative.update_layout(
        xaxis_title="Date",
        yaxis_title="Cumulative Spending ($)",
        hovermode='x unified',
        yaxis=dict(tickprefix="$")
    )
    
    # Add annotation for total
    total_spent = df_expenses_sorted['cumulative_spending'].iloc[-1]
    fig_cumulative.add_annotation(
        x=df_expenses_sorted['date'].iloc[-1],
        y=total_spent,
        text=f"Total: ${total_spent:.2f}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#e74c3c",
        ax=-60,
        ay=-40,
        font=dict(size=14, color="#e74c3c", family="Arial Black")
    )
    
    st.plotly_chart(fig_cumulative, use_container_width=True)
    
    st.info("💡 **How to read this chart:** The line shows your total spending accumulating over time. Steep sections = heavy spending periods. Flat sections = no/minimal spending.")
    
    # Category breakdown over time
    st.markdown("#### 📊 Category Spending Trends")
    
    # Determine date range to choose appropriate grouping
    date_range_days = (df_expenses['date'].max() - df_expenses['date'].min()).days
    
    if date_range_days < 60:  # Less than 2 months - use weekly grouping
        df_expenses['time_period'] = df_expenses['date'].dt.to_period('W').apply(lambda r: r.start_time.strftime('%b %d'))
        time_label = 'Week Starting'
        st.info("📅 **Grouping by week** - Upload 2+ months of data to see monthly trends")
    else:  # 2+ months - use monthly grouping
        df_expenses['time_period'] = df_expenses['date'].dt.strftime('%b %Y')
        time_label = 'Month'
        st.info("📅 **Grouping by month** - Showing category spending trends over time")
    
    category_time = df_expenses.groupby(['time_period', 'category'])['abs_amount'].sum().reset_index()
    
    fig_area = px.area(
        category_time,
        x='time_period',
        y='abs_amount',
        color='category',
        title="",
        labels={'time_period': time_label, 'abs_amount': 'Amount ($)', 'category': 'Category'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_area.update_layout(
        xaxis_title=time_label,
        yaxis_title="Spending ($)",
        yaxis=dict(tickprefix="$"),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.15
        )
    )
    st.plotly_chart(fig_area, use_container_width=True)
    
    with st.expander("💡 How to read this chart"):
        st.markdown("""
        - **Each colored layer** represents a spending category
        - **Height of layer** = amount spent in that category
        - **Total height** = total spending for that time period
        - **Growing layers** = increasing spending in that category
        - **Shrinking layers** = decreasing spending
        
        **Tip:** With more months of data, you can spot trends like:
        - Seasonal patterns (holidays, back-to-school)
        - Growing subscription costs
        - Changes in lifestyle spending
        """)


def display_insights(df):
    """Display financial insights and analysis."""
    
    st.subheader("💡 Financial Insights")
    
    # Calculate metrics
    df_expenses = df[df['amount'] < 0].copy()
    df_income = df[df['amount'] > 0].copy()
    
    total_expenses = abs(df_expenses['amount'].sum())
    total_income = df_income['amount'].sum()
    net_flow = total_income - total_expenses
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💸 Total Spending",
            f"${total_expenses:,.2f}",
            delta=None
        )
    
    with col2:
        st.metric(
            "💰 Total Income",
            f"${total_income:,.2f}",
            delta=None
        )
    
    with col3:
        delta_color = "normal" if net_flow >= 0 else "inverse"
        st.metric(
            "📊 Net Cash Flow",
            f"${net_flow:,.2f}",
            delta=f"{'Surplus' if net_flow >= 0 else 'Deficit'}"
        )
    
    st.markdown("---")
    
    # Top merchants
    st.markdown("### 🏪 Top 5 Merchants by Spending")
    
    if not df_expenses.empty:
        df_expenses['merchant'] = df_expenses['description'].apply(extract_merchant_name)
        top_merchants = df_expenses.groupby('merchant')['abs_amount'].sum().sort_values(ascending=False).head(5)
        
        # Create a nice table
        top_merchants_df = pd.DataFrame({
            'Merchant': top_merchants.index,
            'Total Spent': [f"${x:,.2f}" for x in top_merchants.values],
            'Percentage': [f"{(x/total_expenses*100):.1f}%" for x in top_merchants.values]
        })
        top_merchants_df.index = range(1, len(top_merchants_df) + 1)
        
        st.dataframe(top_merchants_df, use_container_width=True)
    
    st.markdown("---")
    
    # Category breakdown
    st.markdown("### 📂 Spending by Category")
    
    if not df_expenses.empty:
        category_summary = df_expenses.groupby('category').agg({
            'abs_amount': ['sum', 'count', 'mean']
        }).round(2)
        
        category_summary.columns = ['Total ($)', 'Transactions', 'Avg per Transaction ($)']
        category_summary = category_summary.sort_values('Total ($)', ascending=False)
        category_summary['Percentage'] = (category_summary['Total ($)'] / total_expenses * 100).round(1)
        
        st.dataframe(category_summary, use_container_width=True)
    
    # Date range
    st.markdown("---")
    st.markdown("### 📅 Analysis Period")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Start Date:** {df['date'].min().strftime('%Y-%m-%d')}")
    with col2:
        st.write(f"**End Date:** {df['date'].max().strftime('%Y-%m-%d')}")
    with col3:
        days = (df['date'].max() - df['date'].min()).days
        st.write(f"**Duration:** {days} days")


def display_download_section(df):
    """Display download options."""
    
    st.subheader("📥 Download Classified Data")
    
    st.write("Download your transactions with added categories and analysis columns.")
    
    # Select columns to include
    st.markdown("#### Select Columns to Include")
    
    all_columns = df.columns.tolist()
    default_columns = ['date', 'description', 'amount', 'category']
    
    selected_columns = st.multiselect(
        "Columns",
        options=all_columns,
        default=[col for col in default_columns if col in all_columns]
    )
    
    if not selected_columns:
        st.warning("Please select at least one column.")
        return
    
    # Preview
    st.markdown("#### Preview (First 5 Rows)")
    st.dataframe(df[selected_columns].head(), use_container_width=True)
    
    # Download button
    st.markdown("#### Download File")
    
    # Convert to CSV
    csv_buffer = BytesIO()
    df[selected_columns].to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name="classified_transactions.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.info(f"Ready to download {len(df)} transactions with {len(selected_columns)} columns")


if __name__ == "__main__":
    main()

