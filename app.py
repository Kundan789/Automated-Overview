import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- Setup Premium Page Config ---
st.set_page_config(
    page_title="Automated Overview", 
    layout="wide", 
    page_icon="✨",
    initial_sidebar_state="collapsed"
)

# --- Premium UI Custom CSS Injection ---
st.markdown("""
<style>
/* Import Modern Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Apply Global Font */
html, body, [class*="css"]  {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Premium Main Title Styling */
.main-header {
    background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3.5rem !important;
    font-weight: 800 !important;
    margin-bottom: 0px !important;
    padding-bottom: 5px !important;
    text-align: center;
}
.sub-header {
    text-align: center;
    color: #6c757d;
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 30px;
}

/* Glassmorphism Upload Box */
[data-testid="stFileUploadDropzone"] {
    background: rgba(255, 255, 255, 0.05); /* slightly transparent */
    backdrop-filter: blur(10px);
    border: 2px dashed #4ECDC4 !important;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}
[data-testid="stFileUploadDropzone"]:hover {
    background: rgba(78, 205, 196, 0.05);
    border: 2px dashed #FF6B6B !important;
    transform: translateY(-2px);
    box-shadow: 0 15px 35px -10px rgba(0,0,0,0.15);
}

/* Elegant Metric Cards */
[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: #4ECDC4;
}
[data-testid="stMetricLabel"] {
    font-weight: 600 !important;
    font-size: 1.1rem !important;
    color: #888;
}

/* Elevated Tab Styling */
div[data-baseweb="tab-list"], [data-testid="stTabs"] {
    gap: 10px;
}
div[data-baseweb="tab"] {
    background-color: transparent;
    border-radius: 8px 8px 0px 0px;
    padding: 10px 20px;
    font-weight: 600;
    transition: border-bottom 0.3s ease;
}
div[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 3px solid #FF6B6B !important;
    background-color: rgba(255, 107, 107, 0.05);
}

/* Pulsing highlight for Tutorial Phase */
.tab-glow {
    animation: pulse-tab 2s infinite;
    border: 2px solid #FFD700 !important;
    border-radius: 12px !important;
    padding: 4px;
}
@keyframes pulse-tab {
    0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.6); }
    70% { box-shadow: 0 0 0 10px rgba(255, 215, 0, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
}

/* Beautiful Sticky Tutorial Box */
.tutorial-box {
    background: linear-gradient(135deg, #fffcf0 0%, #fff9db 100%);
    border-left: 6px solid #FFC107;
    padding: 24px;
    border-radius: 12px;
    margin-top: 20px;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(255, 193, 7, 0.2);
    color: #5c4700;
}
@media (prefers-color-scheme: dark) {
    .tutorial-box {
        background: linear-gradient(135deg, #2c2505 0%, #1a1600 100%);
        border-left: 6px solid #FFD54F;
        color: #ffeba1;
        box-shadow: 0 8px 25px rgba(255, 213, 79, 0.1);
    }
}
.tut-title { font-weight: 800; font-size: 1.4rem; margin-bottom: 12px; }
.tut-list { line-height: 1.8; font-size: 1.05rem; }

/* Custom Button Styling */
button[kind="secondary"] {
    background-color: white !important;
    color: #FF6B6B !important;
    border: 2px solid #FF6B6B !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}
button[kind="secondary"]:hover {
    background-color: #FF6B6B !important;
    color: white !important;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'tutorial_dismissed' not in st.session_state:
    st.session_state['tutorial_dismissed'] = False

if 'file_processed' not in st.session_state:
    st.session_state['file_processed'] = False

if 'just_loaded' not in st.session_state:
    st.session_state['just_loaded'] = False

def file_upload_callback():
    # Triggered precisely when a new file is uploaded
    st.session_state['file_processed'] = False
    st.session_state['tutorial_dismissed'] = False
    st.session_state['just_loaded'] = False

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# --- App Header ---
st.markdown('<div class="main-header">Automated Overview ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload your dataset to instantly get deep insights, beautiful charts, and advanced data health alerts!</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Drop your dataset here (CSV or Excel)", type=['csv', 'xlsx'], on_change=file_upload_callback)

if uploaded_file is not None:
    try:
        # --- Premium Loading Screen Sequence ---
        if not st.session_state.get('file_processed', False):
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown("<br><br><br>", unsafe_allow_html=True)
                col_left, col_mid, col_right = st.columns([1, 2, 1])
                with col_mid:
                    st.markdown("<h2 style='text-align: center; color: #4ECDC4;'>🪄 Magic is happening...</h2>", unsafe_allow_html=True)
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
                    st.session_state['just_loaded'] = True
            
            # Clear loading UI and refresh
            loading_placeholder.empty()
            st.rerun()
            
        else:
            df = st.session_state['df']
            
            # Trigger Celebration Effects
            if st.session_state.get('just_loaded', False):
                st.toast('Dataset processed successfully!', icon='✅')
                st.session_state['just_loaded'] = False
                
            st.success(f"**Successfully loaded `{uploaded_file.name}`!** Explore your insights below.")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- Dismissable Tutorial Banner ---
            if not st.session_state['tutorial_dismissed']:
                # Wrap the tabs area in the 'tab-glow' class dynamically
                st.markdown('<div class="tab-glow">', unsafe_allow_html=True)
                
                tut_container = st.empty()
                with tut_container.container():
                    st.markdown("<div class='tutorial-box'>", unsafe_allow_html=True)
                    col1, col2 = st.columns([0.85, 0.15])
                    with col1:
                        st.markdown("<div class='tut-title'>💡 Quick Tour: Exploring Your Dashboard</div>", unsafe_allow_html=True)
                        st.markdown("""
                        <div class='tut-list'>
                        Check out the glowing menus below to navigate your data:
                        <br>📋 <b>Data Overview</b>: Get a bird's-eye view of your dataset shape and missing values.
                        <br>📈 <b>Interesting Charts</b>: Automatically generated heatmaps and beautiful distribution plots. 
                        <br>🔎 <b>Custom Queries</b>: Build pivot tables and aggregate your numbers completely code-free.
                        <br>🚨 <b>Alerts & Outliers</b>: A senior analyst tool that mathematically detects extreme anomalies!
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown("<br><br>", unsafe_allow_html=True) # visual spacing
                        if st.button("Close Tour ❌", key="dismiss_tut"):
                            st.session_state['tutorial_dismissed'] = True
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                    
            # --- The Premium Menus (Tabs) ---
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            tab1, tab2, tab3, tab4 = st.tabs(["📋 Data Overview (EDA)", "📈 Interesting Charts", "🔎 Custom Queries", "🚨 Alerts & Outliers"])
            
            with tab1:
                st.markdown("<br>", unsafe_allow_html=True)
                # Create a nice top-level metrics row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Total Rows", f"{df.shape[0]:,}")
                with m2:
                    st.metric("Total Columns", f"{df.shape[1]:,}")
                with m3:
                    st.metric("Number Fields", len(numeric_cols))
                
                st.divider()
                
                st.subheader("Raw Data Preview")
                st.dataframe(df.head(15), use_container_width=True)
                
                st.divider()
                
                st.subheader("Data Types & Missing Values Tracker")
                missing_data = pd.DataFrame({
                    'Data Type': df.dtypes,
                    'Missing Values': df.isnull().sum(),
                    '% Missing': (df.isnull().sum() / len(df) * 100).round(2)
                })
                # Highlight columns with high missing %
                def highlight_missing(s):
                    return ['background-color: #ffcccc' if val > 20 else '' for val in s]
                
                st.dataframe(missing_data.sort_values(by='% Missing', ascending=False), use_container_width=True)
                
                st.divider()
                
                st.subheader("Detailed Descriptive Statistics")
                if numeric_cols:
                    st.dataframe(df[numeric_cols].describe().T, use_container_width=True)
                else:
                    st.info("No numeric columns found for descriptive statistics.")
                    
            with tab2:
                st.markdown("<br>", unsafe_allow_html=True)
                
                if numeric_cols and len(numeric_cols) >= 2:
                    st.subheader("Interactive Scatter Explorer")
                    st.caption("Discover relationships between two metrics. Color-code the dots by category for deeper insights!")
                    
                    scat_col1, scat_col2, scat_col3 = st.columns(3)
                    with scat_col1:
                        x_axis = st.selectbox("X-Axis", numeric_cols, index=0)
                    with scat_col2:
                        y_axis = st.selectbox("Y-Axis", numeric_cols, index=1)
                    with scat_col3:
                        color_axis = st.selectbox("Color By (Optional)", ["None"] + categorical_cols)
                    
                    color_arg = None if color_axis == "None" else color_axis
                    fig_scat = px.scatter(
                        df, x=x_axis, y=y_axis, color=color_arg, 
                        hover_data=df.columns, opacity=0.7,
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig_scat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Plus Jakarta Sans")
                    st.plotly_chart(fig_scat, use_container_width=True)
                    
                    st.divider()
                    st.subheader("Correlation Heatmap")
                    corr = df[numeric_cols].corr()
                    fig_corr = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="Tealrose")
                    fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Plus Jakarta Sans")
                    st.plotly_chart(fig_corr, use_container_width=True)
                    st.divider()
                    
                if numeric_cols:
                    st.subheader("Numerical Distributions")
                    st.caption("Select a metric to view how its values are spread out, including a box plot for quartiles.")
                    num_col_to_plot = st.selectbox("Select a numeric column:", numeric_cols, key="dist_num")
                    
                    fig_hist = px.histogram(
                        df, x=num_col_to_plot, marginal="box", 
                        hover_data=df.columns, color_discrete_sequence=['#4ECDC4']
                    )
                    fig_hist.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Plus Jakarta Sans", bargap=0.1)
                    st.plotly_chart(fig_hist, use_container_width=True)
                    st.divider()
                    
                if categorical_cols:
                    st.subheader("Categorical Breakdowns")
                    st.caption("Viewing the top occurrences for categorical data as an interactive Donut Chart.")
                    cat_col_to_plot = st.selectbox("Select a category column:", categorical_cols, key="comp_cat")
                    
                    top_cats = df[cat_col_to_plot].value_counts().nlargest(10).reset_index()
                    top_cats.columns = [cat_col_to_plot, 'Count']
                    
                    fig_pie = px.pie(
                        top_cats, values='Count', names=cat_col_to_plot, hole=0.45,
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Plus Jakarta Sans", showlegend=False)
                    
                    # Display Donut and Bar charts side-by-side or stacked
                    st.plotly_chart(fig_pie, use_container_width=True)
                    
                    st.divider()
                    st.subheader("Category Frequencies (Bar Chart)")
                    st.caption("A bar chart makes it easy to precisely compare the exact sizes of different categories.")
                    fig_bar = px.bar(
                        top_cats, x=cat_col_to_plot, y='Count', 
                        color='Count', color_continuous_scale="Sunset"
                    )
                    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Plus Jakarta Sans", showlegend=False)
                    st.plotly_chart(fig_bar, use_container_width=True)
                    st.divider()
                    
            with tab3:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### 🔎 Visual Query Builder")
                st.markdown("No SQL? No problem. Use the dropdowns to group and aggregate your data instantly.")
                
                if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                    q_col1, q_col2, q_col3 = st.columns(3)
                    with q_col1:
                        col_group = st.selectbox("1. Group By (Category)", categorical_cols + numeric_cols)
                    with q_col2:
                        col_val = st.selectbox("2. Value to Calculate (Numeric)", numeric_cols)
                    with q_col3:
                        agg_func = st.selectbox("3. Aggregation Type", ["sum", "mean", "median", "min", "max", "count"])
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if st.button("🚀 Calculate Query", use_container_width=True):
                        with st.spinner("Crunching numbers..."):
                            result = df.groupby(col_group)[col_val].agg(agg_func).reset_index()
                            # Sort and get top 30
                            result = result.sort_values(by=col_val, ascending=False).head(30) 
                            
                            result_col_name = f"{agg_func.capitalize()} of {col_val}"
                            result.columns = [col_group, result_col_name]
                            
                            st.markdown(f"**Top 30 Results:** {result_col_name} grouped by {col_group}")
                            
                            fig_res = px.bar(
                                result, x=col_group, y=result_col_name, 
                                color=result_col_name, color_continuous_scale="Purp"
                            )
                            fig_res.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_family="Plus Jakarta Sans", showlegend=False)
                            st.plotly_chart(fig_res, use_container_width=True)
                            
                            with st.expander("View Raw Data Table"):
                                st.dataframe(result, use_container_width=True)
                                csv_data = convert_df_to_csv(result)
                                st.download_button(
                                    label="📥 Download Result as CSV",
                                    data=csv_data,
                                    file_name='custom_query_result.csv',
                                    mime='text/csv',
                                )
                else:
                    st.info("You need at least one numeric column and one categorical to perform aggregations.")
                    
            with tab4:
                st.markdown("<br>", unsafe_allow_html=True)
                st.header("Automated Health Checks")
                
                missing_tot = df.isnull().sum().sum()
                if missing_tot > 0:
                    st.error(f"**Attention needed:** We found **{missing_tot:,}** missing data points across your dataset. Check the Data Overview tab to see which columns are the worst offenders.")
                else:
                    st.success("✅ **Perfect Health:** Your dataset has 100% data completion with zero missing values.")
                    
                st.divider()
                
                st.subheader("Statistical Outlier Scanner (IQR Method)")
                st.markdown("Use this to detect mathematically extreme values (anomalies) in your numerical data.")
                
                if numeric_cols:
                    outlier_col = st.selectbox("Select a metric to scan for outliers", numeric_cols)
                    
                    Q1 = df[outlier_col].quantile(0.25)
                    Q3 = df[outlier_col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    outliers = df[(df[outlier_col] < lower_bound) | (df[outlier_col] > upper_bound)]
                    
                    if not outliers.empty:
                        percentage = (len(outliers) / len(df)) * 100
                        st.warning(f"🚨 **Analysis Complete:** Found **{len(outliers):,}** severe outliers in **{outlier_col}**. This represents {percentage:.1f}% of your data.")
                        st.caption(f"Reason: Values fell outside the expected bounds of {lower_bound:.2f} to {upper_bound:.2f}")
                        
                        st.dataframe(outliers, use_container_width=True)
                        
                        csv_outliers = convert_df_to_csv(outliers)
                        st.download_button(
                            label="📥 Download Outliers as CSV",
                            data=csv_outliers,
                            file_name='detected_outliers.csv',
                            mime='text/csv',
                        )
                    else:
                        st.success(f"✅ **Analysis Complete:** No significant extreme values detected in **{outlier_col}**.")
                else:
                    st.info("No numeric columns available to scan for outliers.")

            # Close the glow wrapper if tut is not dismissed
            if not st.session_state['tutorial_dismissed']:
                st.markdown('</div>', unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"A critical error occurred while processing the file: {e}")
