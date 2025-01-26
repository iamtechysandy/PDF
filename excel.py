import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
import io


def run():
    st.title("Excel Comparator")
    st.markdown("### Upload two Excel files to perform a detailed comparison of rows and columns.")
    st.markdown("---")

    # File uploaders
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Upload First Excel File", type=["xlsx"])
    with col2:
        file2 = st.file_uploader("Upload Second Excel File", type=["xlsx"])

    if file1 and file2:
        # Load column names for user selection
        df1_sample = pd.read_excel(file1, nrows=5)
        df2_sample = pd.read_excel(file2, nrows=5)
        common_columns = list(set(df1_sample.columns) & set(df2_sample.columns))

        if len(common_columns) > 0:
            # Sidebar for user inputs
            st.sidebar.subheader("Matching Options")
            key_columns = st.sidebar.multiselect(
                "Select Key Columns for Matching Rows", options=common_columns, default=common_columns[:1]
            )
            compare_columns = st.sidebar.multiselect("Select Columns for Detailed Comparison", options=common_columns)
            case_sensitive = st.sidebar.checkbox("Case-Sensitive Comparison", value=True)
            fuzzy_match = st.sidebar.checkbox("Enable Fuzzy Matching", value=False)

            if st.button("Compare Files"):
                # Perform comparison
                matched, unmatched, differences = compare_excels(
                    file1, file2, key_columns, compare_columns, case_sensitive, fuzzy_match
                )

                # Display results
                tab1, tab2, tab3 = st.tabs(["Matched Rows", "Unmatched Rows", "Column Differences"])
                with tab1:
                    st.subheader("Matched Rows")
                    st.dataframe(matched)
                with tab2:
                    st.subheader("Unmatched Rows")
                    st.dataframe(unmatched)
                with tab3:
                    st.subheader("Column Differences")
                    st.dataframe(differences)

                # Visualization
                st.subheader("Comparison Summary")
                summary = pd.DataFrame({
                    "Category": ["Matched Rows", "Unmatched Rows"],
                    "Count": [len(matched), len(unmatched)],
                })
                fig, ax = plt.subplots()
                ax.bar(summary["Category"], summary["Count"], color=["#4CAF50", "#FF5733"])
                st.pyplot(fig)

                # Downloadable Excel report
                output_buffer = io.BytesIO()
                with pd.ExcelWriter(output_buffer, engine="xlsxwriter") as writer:
                    matched.to_excel(writer, sheet_name="Matched Rows", index=False)
                    unmatched.to_excel(writer, sheet_name="Unmatched Rows", index=False)
                    differences.to_excel(writer, sheet_name="Column Differences", index=False)

                st.download_button(
                    "Download Comparison Report",
                    data=output_buffer.getvalue(),
                    file_name="comparison_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        else:
            st.error("No common columns found between the two files.")


# Helper Functions
def compare_excels(file1, file2, key_columns, compare_columns, case_sensitive, fuzzy_match):
    """
    Compare two Excel files based on key and comparison columns.
    """
    # Load Excel files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Optional case-insensitive normalization
    if not case_sensitive:
        df1[key_columns] = df1[key_columns].applymap(lambda x: str(x).lower() if isinstance(x, str) else x)
        df2[key_columns] = df2[key_columns].applymap(lambda x: str(x).lower() if isinstance(x, str) else x)

    # Merge DataFrames
    merged_df = pd.merge(df1, df2, on=key_columns, how="outer", suffixes=('_File1', '_File2'), indicator=True)

    # Matched and unmatched rows
    matched = merged_df[merged_df["_merge"] == "both"]
    unmatched = merged_df[merged_df["_merge"] != "both"]

    # Column-wise differences
    differences = []
    for col in compare_columns:
        col_file1 = f"{col}_File1"
        col_file2 = f"{col}_File2"
        if col_file1 in merged_df.columns and col_file2 in merged_df.columns:
            mismatched = merged_df[merged_df[col_file1] != merged_df[col_file2]].copy()
            if fuzzy_match:
                mismatched["Difference"] = mismatched.apply(
                    lambda row: f"File1: {row[col_file1]} | File2: {row[col_file2]} | Similarity: {round(SequenceMatcher(None, str(row[col_file1]), str(row[col_file2])).ratio() * 100, 2)}%",
                    axis=1,
                )
            else:
                mismatched["Difference"] = mismatched.apply(
                    lambda row: f"File1: {row[col_file1]} | File2: {row[col_file2]}", axis=1,
                )
            differences.append(mismatched[["Difference"] + key_columns])

    return matched, unmatched, pd.concat(differences, ignore_index=True) if differences else pd.DataFrame()
