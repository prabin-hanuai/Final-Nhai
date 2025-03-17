import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score

# Set wide layout
st.set_page_config(
    page_title="Road Infrastructure Analysis Dashboard",
    page_icon="🛣️",
    layout="wide"
)

def show_main_page():
    # Header section
    st.title("Road Infrastructure Analysis Dashboard")
    st.markdown("---")
    
    # Main features explanation
    col1, col2,col3 = st.columns(3)
    
    with col1:
        st.header("📊 Report Generation")
        st.markdown("""
        ### Key Features
        
        **Input Requirements:**
        - PIU (Project Implementation Unit) Excel file
        - RA (RoadAthena AI Survey) Excel file
        - RSA (Road Safety Audit) Excel file
        
        **Report Components:**
        - Comprehensive road signage inventory analysis
        - Multi-level gap analysis comparing:
          * NHAI/PIU records
          * RoadAthena AI survey findings
          * RSA recommendations
        - Chainage-wise breakdown
        - Detailed furniture asset analysis
        
        **Generated Report:**
        - Professional Word document including:
          * Comparative analysis tables
          * Statistical visualizations
          * Chainage-wise detailed breakdown
          * Gap analysis summaries
        
        ➡️ Select **Generate Report NHAI** in the sidebar
        """)
        
    with col2:
        st.header("📈 Analysis Dashboard")
        st.markdown("""
        ### Key Features
        
        **Data Analysis:**
        - Compare measurement methodologies:
          * Vinci (Expert) measurements
          * RoadAthena (AI) measurements
        
        **Statistical Metrics:**
        - Correlation Analysis:
          * Pearson correlation
          * Spearman correlation
        - Error Measurements:
          * Mean Absolute Error (MAE)
          * Mean Squared Error (MSE)
          * Root Mean Squared Error (RMSE)
          * R-squared value
        - Point Agreement Analysis
        
        **Interactive Visualizations:**
        - Density comparison scatter plots
        - Chainage-wise density comparison
        - Residuals analysis plot
        - Filterable by:
          * Chainage
          * Type
        
        ➡️ Select **Analysis of Pavement and Furniture Reports** in the sidebar
        """)
    with col3:
        st.markdown("""
        ### Quick Navigation
        
        Choose your task:
        """)
        
        # Navigation buttons
        if st.button("📊 Generate Reports", use_container_width=True):
            st.switch_page("pages/1_Generate Report NHAI.py")
        
        if st.button("📈 Analyze Data", use_container_width=True):
            st.switch_page("pages/2_Analysis of Pavement and Furniture Reports.py")
    
    # Quick start guide
    st.markdown("---")
    st.header("🚀 Quick Start Guide")
    
    st.subheader("For Report Generation:")
    st.markdown("""
    1. Select 'Generate Report NHAI' from the sidebar
    2. Upload your PIU Excel file (NHAI records)
    3. Upload RA Excel file (RoadAthena AI survey data)
    4. Upload RSA Excel file (Road Safety Audit recommendations)
    5. Review the processed data and visualizations
    6. Generate and download the comprehensive Word report
    """)
    
    st.subheader("For Analysis Dashboard:")
    st.markdown("""
    1. Select 'Analysis of Pavement and Furniture Reports' from the sidebar
    2. Upload your Excel file containing both Vinci and RoadAthena measurements
    3. Use the filters to select specific chainages or types
    4. Explore the interactive visualizations:
       - Compare density measurements
       - Analyze statistical metrics
       - Review residuals analysis
    5. Interpret the point agreement analysis and correlation metrics
    """)
    
    # Additional information
    st.markdown("---")
    st.header("ℹ️ About")
    st.markdown("""
    This application streamlines road infrastructure analysis through:
    - Automated report generation combining multiple data sources
    - Statistical comparison of manual and AI-based measurements
    - Interactive visualization tools for data interpretation
    - Comprehensive gap analysis for road furniture inventory
    
    The system helps identify discrepancies between different survey methods and provides actionable insights for road infrastructure management.
    """)

if __name__ == "__main__":
    show_main_page()