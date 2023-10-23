import openai
import streamlit as st
import matplotlib

def run_request(question_to_ask, key, model_type):
    openai.api_key = key
    task = "Generate Python Code Script."

    if model_type == "gpt-4" or model_type == "gpt-3.5-turbo" :
        task += " The script should only include code, no comments."
        try:
            response = openai.ChatCompletion.create(
                model=model_type,
                messages=[
                    {"role": "system", "content": task},
                    {"role": "user", "content": question_to_ask}
                ]
            )
            llm_response = response["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None

    elif model_type in ["text-davinci-003", "gpt-3.5-turbo-instruct"]:
        try:
            response = openai.Completion.create(
                engine=model_type,
                prompt=question_to_ask,
                temperature=0,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["plt.show()"])
            
            llm_response = response["choices"][0]["text"]
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None

    else:
        st.write(f"Selected model: {model_type}")

        raise ValueError("Unknown model type selected.")

    return format_response(llm_response)




def format_response( res):
    # Remove the load_csv from the answer if it exists
    csv_line = res.find("read_csv")
    if csv_line > 0:
        return_before_csv_line = res[0:csv_line].rfind("\n")
        if return_before_csv_line == -1:
            # The read_csv line is the first line so there is nothing to need before it
            res_before = ""
        else:
            res_before = res[0:return_before_csv_line]
        res_after = res[csv_line:]
        return_after_csv_line = res_after.find("\n")
        if return_after_csv_line == -1:
            # The read_csv is the last line
            res_after = ""
        else:
            res_after = res_after[return_after_csv_line:]
        res = res_before + res_after
    return res

def format_question(primer_desc, primer_code, question, model_type):
    return f'"""\n{primer_desc}{question}\n"""\n{primer_code}'


def get_primer(df_dataset, df_name):
    # Primer function to take a dataframe and its name
    # and the name of the columns
    # and any columns with less than 20 unique values it adds the values to the primer
    # and horizontal grid lines and labeling
    primer_desc = "Given a dataframe named df sourced from data_file.csv with columns: " \
                  + "', '".join(str(x) for x in df_dataset.columns) + "'. "
    for i in df_dataset.columns:
        unique_values = df_dataset[i].drop_duplicates()
        if len(unique_values) < 20 and df_dataset.dtypes[i] == "O":
            primer_desc += "\nThe column '" + i + "' contains categorical values: '" + \
                           "', '".join(str(x) for x in unique_values) + "'. "
        elif df_dataset.dtypes[i] in ["int64", "float64"]:
            primer_desc += "\nThe column '" + i + "' is of type " + str(df_dataset.dtypes[i]) + " with numeric data. "
    primer_desc += "\nEnsure you label the x and y axes appropriately. Add a relevant title and set the fig suptitle as empty."
    primer_desc += "\nUsing Python 3.9.12, please provide an answer to the textual response as a financial advisor and plot the graph to visualize where appropriate."
    
    # Ensuring that the dataframe assignment is specific and no other df assignments are added by the model
    primer_code = "import pandas as pd \nimport matplotlib.pyplot as plt\n"
    primer_code = primer_code + "fig,ax = plt.subplots(1,1,figsize=(10,4))\n"
    primer_code = primer_code + "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False) \n"
   
# ONLY use 'df' for the dataframe. DO NOT add any new df assignment or df loading lines.
    primer_code = primer_code + "df=" + df_name + ".copy()\n"

    return primer_desc, primer_code







# Load the data
#df = pd.read_csv('data_file.csv')

# Generate the primer
#primer_desc, primer_code = get_primer(df, 'df')

# Run the request
#response = run_request(primer_desc, primer_code, 'Plot a bar chart of the "Amount" column for each "Account Name".', 'gpt-3')

# Execute the generated code
#exec(response)

#def format_response(res):
#        # Remove incomplete pd assignment
#    if "df = pd." in res:
#        res = res.replace("df = pd.", "").strip()

#       csv_line = res.find("read_csv")
#   if csv_line > 0:
#       res_before = res[:csv_line].rstrip()
#       res_after = res[csv_line:].split("\n", 1)[1].lstrip()
#       res = res_before + "\n" + res_after
#   return res 