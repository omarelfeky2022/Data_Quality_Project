import io
import streamlit as st
import pandas as pd
from io import StringIO
from methods import *

# Main function that handles the app logic
def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Data Quality Analysis")
    
    # File upload section
    uploaded_file = st.sidebar.file_uploader("Upload Dataset", type=["csv", "xlsx"], key='file_uploader')
    
    if uploaded_file is not None:
        # Load dataset if not already in session
        if 'data' not in st.session_state:
            try:
                if uploaded_file.name.endswith(".csv"):
                    csv_file = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    df = pd.read_csv(csv_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)
                st.session_state['data'] = df
                st.sidebar.success("Dataset uploaded successfully!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
        else:
            df = st.session_state['data'].copy()

        st.header("Original DataFrame")
        st.write(df)

        # Dataset info
        if st.sidebar.button("Dataset info", key='show_data_btn'):
            reset_all_flags()
            st.session_state['show_data'] = True
            if df is not None:
                buffer = io.StringIO()
                df.info(buf=buffer)
                dataset_info = buffer.getvalue()

        if st.session_state.get('show_data', False):
            st.header("Dataset Information:")
            st.text(dataset_info)
            reset_all_flags()

        # Describe Data
        if st.sidebar.button("Describe Data", key='describe_data_btn'):
            reset_all_flags()
            st.session_state['describe_data'] = True

        if st.session_state.get('describe_data', False):
            st.header("Data Description")
            st.table(describe_data(df))
            reset_all_flags()

        # Data Type Analysis
        if st.sidebar.button("Data Type Analysis", key='data_type_btn'):
            reset_all_flags()
            st.session_state['data_type_analysis_clicked'] = True

        if st.session_state.get('data_type_analysis_clicked', False):
            df = data_types_analysis(df)

        if st.session_state.get('type_converted', False):
            st.write("Updated DataFrame:")
            st.write(df)
            st.session_state['type_converted'] = False
            reset_all_flags()

        # Column Name Analysis
        if st.sidebar.button("Column Name Analysis", key='col_name_btn'):
            reset_all_flags()
            st.session_state['column_name_analysis_clicked'] = True

        if st.session_state.get('column_name_analysis_clicked', False):
            df = column_names_analysis(df)
            st.session_state['column_name_analysis_clicked'] = True

        if st.session_state.get('columns_renamed', False):
            st.write(df)
            st.session_state['columns_renamed'] = False
            reset_all_flags()

        # Missing Value Analysis
        if st.sidebar.button("Missing Value Analysis", key='missing_val_btn'):
            reset_all_flags()
            st.session_state['missing_analysis_run'] = True

        if st.session_state.get('missing_analysis_run', False):
            st.header("Missing Value Analysis")
            missing_value_analysis(df)
            st.session_state['missing_analysis_run'] = False

        method = st.sidebar.selectbox("Select Method", ["mean", "median", "mode", "drop"], key="missing_method")
        column = st.sidebar.selectbox("Select Column (optional)", df.columns, key="missing_col")
        
        if st.sidebar.button("Handle Missing Values", key='handle_missing_btn'):
            reset_all_flags()
            df = handle_missing_values(df, method, column)
            st.session_state['data'] = df
            st.session_state['missing_values_handled'] = True

        if st.session_state.get('missing_values_handled', False):
            st.header("Data after Handling Missing Values")
            st.write(df)
            missing_value_analysis(df)
            st.session_state['missing_values_handled'] = False

        # Handle Duplicates
        if st.sidebar.button("Handle Duplicates", key='handle_duplicates_btn'):
            reset_all_flags()
            st.session_state['handle_duplicates_clicked'] = True

        if st.session_state.get('handle_duplicates_clicked', False):
            df = handle_duplicates(df)

        if st.session_state.get('duplicates_handled', False):
            st.header("Data after Handling Duplicates")
            st.write(df)
            st.session_state['duplicates_handled'] = False

        # Outlier Analysis
        column_for_outlier = st.sidebar.selectbox("Select Column for Outlier Analysis", df.select_dtypes(include=['float64', 'int64']).columns, key="outlier_col")
        if st.sidebar.button("Outlier Analysis", key='outlier_analysis_btn'):
            reset_all_flags()
            st.session_state['outlier_analysis_run'] = True
        
        if st.session_state.get('outlier_analysis_run', False):
            st.header("Outlier Analysis")
            lower_bound, upper_bound = outlier_analysis(df, column_for_outlier)
            if lower_bound is not None and upper_bound is not None:
                outlier_method = st.sidebar.selectbox("Select Outlier Handling Method", ['clip', 'drop'], key="outlier_method")
                if st.sidebar.button("Handle Outliers", key='handle_outliers_btn'):
                    df = handle_outliers(df, column_for_outlier, lower_bound, upper_bound, outlier_method)
                    st.session_state['data'] = df
                    st.session_state['outliers_handled'] = True
                    reset_all_flags()

        if st.session_state.get('outliers_handled', False):
            st.header("Data after Handling Outliers")
            st.write(df)
            st.session_state['outliers_handled'] = False

        # Data Visualization
        column_to_visualize = st.sidebar.selectbox("Select Column for Visualization", df.columns, key="visualize_col")
        if st.sidebar.button("Visualize Data", key='visualize_data_btn'):
            reset_all_flags()
            st.session_state['visualize_data_run'] = True

        if st.session_state.get('visualize_data_run', False):
            st.header("Data Visualization")
            fig1, fig2 = visualize_data(df, column_to_visualize)
            st.pyplot(fig1)
            st.pyplot(fig2)
            st.session_state['visualize_data_run'] = False

        # Correlation Matrix
        if st.sidebar.button("Correlation Matrix", key='correlation_btn'):
            reset_all_flags()
            st.session_state['correlation_run'] = True

        if st.session_state.get('correlation_run', False):
            st.header("Correlation Matrix")
            fig = correlation_matrix(df)
            if fig is not None:
                st.pyplot(fig)
            st.session_state['correlation_run'] = False

        # Download dataset
        if st.sidebar.button("Download dataset", key='download_btn'):
            download_dataset(df)

if __name__ == "__main__":
    main()
