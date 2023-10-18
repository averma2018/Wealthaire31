import openai
from langchain import HuggingFaceHub, LLMChain, PromptTemplate

def run_request(question_to_ask, model_type, key, alt_key=None):
    task = "Generate Python Code Script."

    if model_type in ["gpt-4", "gpt-3.5-turbo"]:
        if model_type == "gpt-4":
            task += " The script should only include code, no comments."
        openai.api_key = key
        response = openai.ChatCompletion.create(
            model=model_type,
            messages=[
                {"role": "system", "content": task},
                {"role": "user", "content": question_to_ask}
            ]
        )
        llm_response = response["choices"][0]["message"]["content"]

    elif model_type in ["text-davinci-003", "gpt-3.5-turbo-instruct"]:
        openai.api_key = key
        response = openai.Completion.create(
            engine=model_type,
            prompt=question_to_ask,
            temperature=0,
            max_tokens=500
        )
        llm_response = response["choices"][0]["text"]

    else:
        if not alt_key:
            raise ValueError("An alternative key is required for the selected model type.")
        llm = HuggingFaceHub(huggingfacehub_api_token=alt_key, repo_id="codellama/" + model_type)
        llm_prompt = PromptTemplate.from_template(question_to_ask)
        llm_chain = LLMChain(llm=llm, prompt=llm_prompt)
        llm_response = llm_chain.predict()

    return format_response(llm_response)


def format_response(res):
    csv_line = res.find("read_csv")
    if csv_line > 0:
        res_before = res[:csv_line].rstrip()
        res_after = res[csv_line:].split("\n", 1)[1].lstrip()
        res = res_before + "\n" + res_after
    return res


def format_question(primer_desc, primer_code, question, model_type):
    if model_type == "Code Llama":
        instructions = "\nDo not use the 'c' argument in the plot function. Use 'color' and pass color names like 'green', 'red', 'blue'."
        primer_desc = primer_desc.format(instructions)
    return f'"""\n{primer_desc}{question}\n"""\n{primer_code}'

import pandas as pd

def get_primer(df_dataset):

  primer_desc = ""
  primer_code = ""

  if df_dataset is None:
    return "", ""

  for col in df_dataset.columns:

    if df_dataset[col].dtype == "object":
      values = "','".join(map(str, df_dataset[col].unique()))
      primer_desc += f"\nColumn '{col}' has values '{values}'"

    elif df_dataset[col].dtype in ["int64", "float64"]:
      primer_desc += f"\nColumn '{col}' has numeric values"

  primer_code = """
  import pandas as pd
  import matplotlib.pyplot as plt
  
  fig, ax = plt.subplots(figsize=(10, 4))
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)  

  df = pd.DataFrame() # dataframe
  """
  
  primer_desc += "\n\nUsing Python 3.9.12 and dataframe df, graph:"

  return primer_desc, primer_code
