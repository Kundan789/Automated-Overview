import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(page_title="Automated Overview", layout="wide", page_icon="📊")

# --- Session State Initialization ---
if 'tutorial_dismissed' not in st.session_state:
    st.session_state['tutorial_dismissed'] = False

if 'file_processed' not in st.session_state:
    st.session_state['file_processed'] = False

def file_upload_callback():
    # Triggered precisely when a new file is uploaded
    st.session_state['file_processed'] = False
    st.session_state['tutorial_dismissed'] = False

st.title("📊 Automated Overview")
st.markdown("Upload your dataset to instantly get deep insights, beautiful charts, and advanced data health alerts!")

uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=['csv', 'xlsx'], on_change=file_upload_callback)

if uploaded_file is not None:
    try:
        # --- Premium Loading Screen Sequence ---
        if not st.session_state.get('file_processed', False):
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown("<br><br><br>", unsafe_allow_html=True)
                col_left, col_mid, col_right = st.columns([1, 2, 1])
                with col_mid:
                    st.markdown("<h2 style='text-align: center;'>🪄 Magic is happening...</h2>", unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.markdown("#### 📂 Extracting file structure...")
                    for i in range(1, 15):
                        progress_bar.progress(i)
                        time.sleep(0.04)
                    
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                        
                    status_text.markdown("#### 🔍 Profiling data columns & types...")
                    for i in range(15, 60):
                        progress_bar.progress(i)
                        time.sleep(0.02)
                    
                    status_text.markdown("#### 📈 Generating visual insights...")
                    for i in range(60, 95):
                        progress_bar.progress(i)
                        time.sleep(0.02)
                        
                    st.session_state['df'] = df
                    st.session_state['file_processed'] = True
                    
                    for i in range(95, 101):
                        progress_bar.progress(i)
                        time.sleep(0.02)
                    status_text.markdown("#### ✨ Analysis complete!")
                    time.sleep(0.5)
            
            # Clear loading UI and refresh to show the actual UI
            loading_placeholder.empty()
            st.rerun()
            
        else:
            df = st.session_state['df']
            st.success(f"Successfully loaded **{uploaded_file.name}**")
            
            # --- Dismissable Tutorial Banner & HIGHLIGHT CSS ---
            if not st.session_state['tutorial_dismissed']:
                # Inject Custom CSS to make the TABS pulse and highlight
                st.markdown("""
                <style>
                /* Highlight the Streamlit tabs container dynamically */
                div[data-baseweb="tab-list"], [data-testid="stTabs"] {
                    border: 3px solid #FFD700 !important;
                    background-color: rgba(255, 215, 0, 0.05) !important;
                    border-radius: 8px !important;
                    animation: pulse-tab 1.5s infinite;
                    padding: 8px;
                    transition: all 0.3s ease-in-out;
                }
                
                @keyframes pulse-tab {
                    0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
                    70% { box-shadow: 0 0 0 12px rgba(255, 215, 0, 0); }
                    100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
                }
                
                .tutorial-box {
                    background-color: #fff3cd; /* Soft yellow warning color */
                    border-left: 6px solid #ffc107; /* Amber accent */
                    padding: 15px 20px;
                    border-radius: 8px;
                    margin-top: 10px;
                    margin-bottom: 25px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    color: #856404;
                }
                @media (prefers-color-scheme: dark) {
                    .tutorial-box {
                        background-color: #332b00;
                        border-left: 6px solid #cca300;
                        color: #ffdf80;
                    }
                }
                </style>
                """, unsafe_allow_html=True)
                
                tut_container = st.empty()
                with tut_container.container():
                    st.markdown("<div class='tutorial-box'>", unsafe_allow_html=True)
                    col1, col2 = st.columns([0.85, 0.15])
                    with col1:
                        st.subheader("💡 Tutorial: See the glowing menus below?")
                        st.markdown("""
                        Click through the **highlighted tabs** to explore your data:
                        - **Data Overview**: Missing values and basic stats.
                        - **Interesting Charts**: Automatic heatmaps and distributions. 
                        - **Custom Queries**: Build custom pivot tables easily.
                        - **Alerts & Outliers**: Discover anomalies instantly.
                        """)
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True) # visual spacing
                        if st.button("Got it! ❌", key="dismiss_tut"):
                            st.session_state['tutorial_dismissed'] = True
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # --- The Menus (Tabs) ---
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Data Overview (EDA)", "📈 Interesting Charts", "🔎 Custom Queries", "🚨 Alerts & Outliers"])
            
            with tab1:
                st.header("1. Data Overview")
                col1, col2, col3 = st.columns(3)
                col1.metric("Rows", f"{df.shape[0]:,}")
                col2.metric("Columns", f"{df.shape[1]:,}")
                col3.metric("Numeric Columns", len(numeric_cols))
                
                st.subheader("Raw Data Preview")
                st.dataframe(df.head(10))
                
                st.subheader("Data Types & Missing Values")
                missing_data = pd.DataFrame({
                    'Data Type': df.dtypes,
                    'Missing Values': df.isnull().sum(),
                    '% Missing': (df.isnull().sum() / len(df) * 100).round(2)
                })
                st.dataframe(missing_data.sort_values(by='% Missing', ascending=False))
                
                st.subheader("Descriptive Statistics")
                if numeric_cols:
                    st.dataframe(df[numeric_cols].describe().T)
                else:
                    st.info("No numeric columns found for descriptive statistics.")
                    
                if categorical_cols:
                    st.subheader("Categorical Summary")
                    cat_summary = df[categorical_cols].describe().T
                    st.dataframe(cat_summary)
                    
            with tab2:
                st.header("2. Automated Visualizations")
                
                if numeric_cols and len(numeric_cols) >= 2:
                    st.subheader("Correlation Heatmap")
                    corr = df[numeric_cols].corr()
                    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", title="Correlation between Numeric Fields")
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                if numeric_cols:
                    st.subheader("Distributions of Numerical Data")
                    num_col_to_plot = st.selectbox("Select a numeric column to view its distribution", numeric_cols)
                    fig_hist = px.histogram(df, x=num_col_to_plot, marginal="box", hover_data=df.columns, title=f"Distribution of {num_col_to_plot}")
                    st.plotly_chart(fig_hist, use_container_width=True)
                    
                if categorical_cols:
                    st.subheader("Categorical Data Counts")
                    cat_col_to_plot = st.selectbox("Select a categorical column", categorical_cols)
                    top_cats = df[cat_col_to_plot].value_counts().nlargest(20).reset_index()
                    top_cats.columns = [cat_col_to_plot, 'Count']
                    fig_bar = px.bar(top_cats, x=cat_col_to_plot, y='Count', title=f"Top 20 categories in {cat_col_to_plot}", color=cat_col_to_plot)
                    st.plotly_chart(fig_bar, use_container_width=True)
                    
            with tab3:
                st.header("3. Custom Query Builder")
                st.markdown("Use this section to group your data and calculate aggregates without writing any code.")
                
                if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                    col_group = st.selectbox("Group By (Category)", categorical_cols + numeric_cols)
                    col_val = st.selectbox("Value to Aggregate (Numeric)", numeric_cols)
                    agg_func = st.selectbox("Aggregation Function", ["sum", "mean", "median", "min", "max", "count"])
                    
                    if st.button("Calculate"):
                        st.subheader("Query Results")
                        result = df.groupby(col_group)[col_val].agg(agg_func).reset_index()
                        result = result.sort_values(by=col_val, ascending=False).head(50) 
                        
                        result_col_name = f"{agg_func.capitalize()} of {col_val}"
                        result.columns = [col_group, result_col_name]
                        st.dataframe(result)
                        
                        fig_res = px.bar(result, x=col_group, y=result_col_name, color=col_group, title=f"{result_col_name} by {col_group}")
                        st.plotly_chart(fig_res, use_container_width=True)
                else:
                    st.info("You need at least one numeric column and one categorical to perform aggregations.")
                    
            with tab4:
                st.header("4. Automated Alerts & Outliers")
                st.subheader("Data Health Alerts")
                missing_tot = df.isnull().sum().sum()
                if missing_tot > 0:
                    st.warning(f"⚠️ Your dataset has a total of **{missing_tot:,}** missing value(s) across all columns.")
                else:
                    st.success("✅ Great! Your dataset has absolutely no missing values.")
                    
                st.subheader("Statistical Outlier Detection (IQR Method)")
                st.markdown("This tool scans your numerical data to find rows with extreme/unusual values.")
                
                if numeric_cols:
                    outlier_col = st.selectbox("Select a column to scan for outliers", numeric_cols)
                    Q1 = df[outlier_col].quantile(0.25)
                    Q3 = df[outlier_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = df[(df[outlier_col] < lower_bound) | (df[outlier_col] > upper_bound)]
                    
                    if not outliers.empty:
                        st.error(f"🚨 Found **{len(outliers):,}** outliers in **{outlier_col}**! (Values outside {lower_bound:.2f} to {upper_bound:.2f})")
                        st.dataframe(outliers.head(50))
                    else:
                        st.success(f"✅ No significant outliers detected in **{outlier_col}**.")
                else:
                    st.info("No numeric columns available to scan for outliers.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
