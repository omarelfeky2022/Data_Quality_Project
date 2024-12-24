Data Quality Analysis
# Data Quality Analysis Tool

This project is a **Streamlit-based web application** designed for comprehensive data quality analysis. It enables users to upload datasets and perform various analyses and operations like missing value handling, outlier detection, and data visualization.

---

## Features

1. **Data Upload**: Upload datasets in CSV or Excel formats.
2. **Data Exploration**:
   - View original data.
   - View dataset information and descriptive statistics.
3. **Analysis Tools**:
   - Analyze and visualize missing values.
   - Perform data type analysis and conversions.
   - Analyze and rename column names.
   - Handle duplicates.
   - Detect and handle outliers.
   - Generate and visualize correlation matrices.
4. **Visualization**: Create histograms, box plots, and heatmaps.
5. **Data Export**: Download the modified dataset as a CSV file.

---

## Getting Started

### Prerequisites
Ensure the following are installed:
- Python 3.7+
- Necessary Python packages listed in `requirements.txt`.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/omarelfeky2022/Data_Quality_Project.git
   ```
   
## File Overview
  - app.py: Contains the main application logic for the Streamlit app.
  - methods.py: Implements utility functions for data analysis and visualization.
  - requirements.txt: Lists the dependencies required to run the application.
## Usage
  - Upload Dataset: Use the sidebar to upload a dataset (CSV or Excel).
  - Perform Analysis:
  - Explore the dataset and generate statistics.
  - Handle missing values, outliers, and duplicates.
  - Rename columns and convert data types.
  - Visualize Data: Use the visualization tools to understand data distributions and correlations.
  - Export Data: Download the processed dataset for further use.
## Dependencies
   The following libraries are used in this project:
  - streamlit - For building the interactive web application.
  - pandas - For data manipulation and analysis.
  - matplotlib and seaborn - For data visualization.
  - openpyxl - For handling Excel files.
