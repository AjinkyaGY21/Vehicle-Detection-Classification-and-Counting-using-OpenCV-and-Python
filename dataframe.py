import pandas as pd

pathi = "results_image.csv"
pathv = "results_video.csv"

def create_dataframe(path):
    try:
        # Specify the correct engine for reading CSV files
        cumulative_results_df = pd.read_csv(path)
        # Drop empty rows
        cumulative_results_df = cumulative_results_df.dropna(how='all')

        # Convert all columns to numeric
        cumulative_results_df = cumulative_results_df.apply(pd.to_numeric, errors='coerce')

        # Create a new DataFrame for the final results
        final_results_df = pd.DataFrame(columns=cumulative_results_df.columns)

        # Iterate through each row in the cumulative results
        for i in range(len(cumulative_results_df)):
            # For the first row, just copy the data as it is
            if i == 0:
                final_results_df = pd.concat([final_results_df, cumulative_results_df.iloc[[i]]])
            else:
                # For subsequent rows, calculate the difference between consecutive rows
                diff_row = cumulative_results_df.iloc[i] - cumulative_results_df.iloc[i - 1]
                final_results_df = pd.concat([final_results_df, pd.Series([None] * len(final_results_df.columns))])
                final_results_df = pd.concat([final_results_df, diff_row])

        # Reset the index of the final results DataFrame
        final_results_df.reset_index(drop=True, inplace=True)

        # Save the final results to a CSV file
        #final_results_df.to_csv("results_image_final.csv", index=False)
        final_results_df.to_csv("results_video_final.csv", index=False)

        # Print the final results DataFrame
        print(final_results_df.fillna(''))

    except Exception as e:
        print(f"An error occurred: {e}")
        # Handle the error or print a specific message

if __name__ == '__main__':
    create_dataframe(pathv)
