import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import re

def describe_data(df):
    # Generates descriptive statistics for the DataFrame.
    return df.describe()

def visualize_data(df, column):
    # Generates histogram and box plot for the selected column.
    fig, ax = plt.subplots()
    sns.histplot(df[column], ax=ax, kde=True)
    plt.title(f"Histogram of {column} with KDE")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df[column], ax=ax2)
    plt.title(f"Box Plot of {column}")
    return fig, fig2

def correlation_matrix(df):
    # Generates a correlation matrix for numeric columns in the DataFrame.
    numeric_cols = df.select_dtypes(include=['float64', 'int64'])
    if numeric_cols.empty:
        st.warning("No numeric columns found for correlation analysis.")
        return None
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(numeric_cols.corr(), annot=True, ax=ax, cmap='coolwarm')
    plt.title("Correlation Matrix (Numeric Columns)")
    return fig

def missing_value_analysis(df):
    # Displays the number of missing values and a heatmap of missing data.
    missing_values = df.isnull().sum()
    st.write("Missing Values per Column:")
    st.table(missing_values)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.isnull(), cmap="viridis", cbar=True, ax=ax)
    plt.title("Missing Values Heatmap")
    st.pyplot(fig)

def handle_missing_values(df, method="mean", column=None):
    # Handles missing values using the specified method.
    if method == "mean":
        if column:
            df[column].fillna(df[column].mean(), inplace=True)
        else:
            df.fillna(df.mean(), inplace=True)
    elif method == "median":
        if column:
            df[column].fillna(df[column].median(), inplace=True)
        else:
            df.fillna(df.median(), inplace=True)
    elif method == "mode":
        if column:
            df[column].fillna(df[column].mode()[0], inplace=True)
        else:
            df.fillna(df.mode().iloc[0], inplace=True)
    elif method == "drop":
        if column:
            df.dropna(subset=[column], inplace=True)
        else:
            df.dropna(inplace=True)
    else:
        st.error("Invalid method for handling missing values.")
    return df

def handle_duplicates(df):
    # Handles duplicate rows in the DataFrame.
    num_duplicates = df.duplicated().sum()
    st.write(f"Number of duplicate rows: {num_duplicates}")
    if 'handle_duplicates_clicked' not in st.session_state:
        st.session_state['handle_duplicates_clicked'] = False
    if num_duplicates > 0:
        show_duplicates = st.checkbox("Show Duplicate Rows", key='show_duplicates')
        if show_duplicates:
            st.write(df[df.duplicated(keep=False)])
        if st.button("Remove Duplicate Rows", key='remove_duplicates'):
            df.drop_duplicates(inplace=True)
            st.session_state['data'] = df
            st.session_state['duplicates_handled'] = True
            reset_all_flags()
            st.success("Duplicate rows removed.")
    return df

def outlier_analysis(df, column):
    # Identifies and displays outliers using the IQR method.
    try:
        numerical_columns = df.select_dtypes(include=['number']).columns
        if len(numerical_columns) == 0:
            raise ValueError("The dataset does not contain any numerical columns.")

        if column not in numerical_columns:
            raise ValueError(f"The selected column '{column}' is not numerical or does not exist in the dataset.")

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

        st.write(f"Number of outliers in {column}: {len(outliers)}")
        if not outliers.empty:
            st.write(outliers)
            show_outliers_vis = st.checkbox("Show outliers visualization", key='show_outliers_vis')
            if show_outliers_vis:
                fig, ax = plt.subplots()
                sns.boxplot(x=df[column], ax=ax)
                sns.scatterplot(x=outliers[column], y=[0]*len(outliers), color='red', marker='o', ax=ax)
                plt.title(f"Box Plot of {column} with Outliers highlighted")
                st.pyplot(fig)

        return lower_bound, upper_bound

    except ValueError as e:
        st.error(str(e))
        return None, None

def handle_outliers(df, column, lower_bound, upper_bound, method='clip'):
    # Handles outliers using the specified method.
    if method == 'clip':
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
        st.success(f"Outliers in {column} have been clipped to the defined bounds.")
    elif method == 'drop':
        df.drop(df[(df[column] < lower_bound) | (df[column] > upper_bound)].index, inplace=True)
        st.success(f"Outliers in {column} have been removed.")
    else:
        st.error("Invalid method for handling outliers.")
    return df

def reset_all_flags():
    # Resets all session state flags.
    keys_to_reset = [
        'show_data', 'describe_data', 'missing_analysis_run',
        'missing_values_handled', 'duplicates_handled',
        'outlier_analysis_run', 'outliers_handled','column_name_analysis_clicked',
        'visualize_data_run', 'correlation_run','type_converted','columns_renamed','data_type_analysis_clicked'
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            st.session_state[key] = False

def process_value(value):
    # Processes a single value to extract numerical data.
    if isinstance(value, str):
        result = re.sub(r"[^0-9.]", "", value)
        if result.count('.') > 1:
            result = result.replace('.', '', result.count('.') - 1)
        try:
            return float(result) if result else None
        except ValueError:
            return None
    elif isinstance(value, (int, float)):
        if pd.isna(value) or np.isinf(value):
            return None
        return value
    else:
        return 0

def process_column_values(column):
    # Processes all values in a column based on specific rules.
    return column.apply(process_value)

def data_types_analysis(df):
    # Displays data type information and allows type conversion.
    st.header("Data Types Analysis")
    st.write(df.dtypes)
    st.subheader("Convert Data Types:")

    if 'data_type_analysis_clicked' not in st.session_state:
        st.session_state['data_type_analysis_clicked'] = False

    if st.session_state['data_type_analysis_clicked']:
        selected_column = st.selectbox("Select a column to convert", df.columns, key="convert_col")
        new_type = st.selectbox("Select the new data type", ["Numeric", "str"], key="new_type")

        if st.button("Convert Data Type", key='convert_btn'):
            try:
                if new_type =="Numeric":
                    df[selected_column] = process_column_values(df[selected_column])
                    df[selected_column] = df[selected_column].astype(float)
                else:
                    df[selected_column] = df[selected_column].astype(str)
                st.success(f"Column '{selected_column}' converted to {new_type} successfully!")
                st.session_state['type_converted'] = True
                st.session_state['data'] = df
            except Exception as e:
                st.error(f"Error converting column '{selected_column}': {e}")

    return df

def column_names_analysis(df):
    # Displays column names and allows renaming.
    st.header("Column Name Analysis")
    st.subheader("Current Column Names:")
    st.write(df.columns)
    st.subheader("Rename Columns:")

    new_column_names = {}
    for col in df.columns:
        new_name = st.text_input(f"Rename '{col}' to:", value=col, key=f"rename_{col}")
        new_column_names[col] = new_name
    rename_button = st.button("Apply Column Renaming", key='rename_btn')
    if rename_button:
        try:
            df.rename(columns=new_column_names, inplace=True)
            st.session_state['data']=df
            st.session_state['columns_renamed'] = True
            reset_all_flags()
            st.success("Columns renamed successfully!")
        except Exception as e:
            st.error(f"Error renaming columns: {e}")
    return df

def download_dataset(df):
    # Provides a download link for the DataFrame as a CSV file.
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="downloaded_data.csv">Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
