# img_viewer.py
try:
    import re
    import os
    import openai
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    
    from configparser import ConfigParser
    
    configur = ConfigParser()
    configur.read('config.ini')

    openai.api_type = "azure"
    openai.api_base = configur.get('azure','api_base')
    openai.api_version = configur.get('azure','api_version')
    openai.api_key = configur.get('azure','openai_key')

    SQL_TABLE_INST_HEADER = "### SQL tables, with their properties:"
except:
    
            sql_desc = values["ip_desc"]
            sql_inst = values["ip_inst"]
            sql_prompt = values["ip_prompt"]
            try:
                # Get list of files in folder
                prompt = []
                prompt.append(SQL_TABLE_INST_HEADER)
                prompt.append
                for ele in sql_desc.splitlines():
                    prompt.append("# "+ele)
                for ele in sql_inst.splitlines():
                    prompt.append("### "+ele)
                for ele in sql_prompt.splitlines():
                    prompt.append("### Q."+ele)
                prompt.append("A.")
                output = ""
                response = openai.Completion.create(
                    engine="maltext",
                    prompt="\n".join(prompt),
                    temperature=0,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    best_of=1,
                    stop=["#",";"]
                )
                try:
                    output = response["choices"][0]["text"]
                    print(response)
                except:
                    output= "NULL response - No choices presented by model.\nPlease reveiw your inputs."
                    print("No output")

            except:
                output = "error"+response
                print("App error")
                pass
            window["op"].update(output)
    window.close()
except:
    print("Error")
    import traceback
    traceback.print_exc()