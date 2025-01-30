
import os, time
from openai import OpenAI
import json

client = OpenAI()


system_instruction = """You are an expert programmer in FAANG company. You task is to help generalists to provide condensed specifications from PR request discussions."""
prompt = """Can you please take a look at this json describing Github PR discussion: <JSON>{json}</JSON>. Please produce super laconic and condense message of changes to be made as instruction to probgammer who knows this repository. Be super attentive to detail, but do not hallucinate anything which is not in the json, please do not list feedback if it has no information, etc, just instructions. OR, if formulating instruction is not possible - describe the issue with the repository which this PR is fixing."""

def query_openai(query, max_retries=5, delay=2):
    retries = 0

    try:

        messages = [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": query}
                        ]
        response = client.chat.completions.create(model="gpt-4o",
                        messages=messages)

        result = response.choices[0].message.content.strip()
        if result:
            #print(response.choices[0].message.content.strip())
            return result
    except Exception as e:
                    print(f"OpenAI query failed: {e}")
                    retries += 1
                    if retries < max_retries:
                        time.sleep(delay * retries)
                    else:
                        raise
    return ""

def summarize_changes(json_obj):
    result = query_openai(prompt.format(json=json_obj))
    return result


if __name__ == "__main__":
      with open('pr_6236_review_comments.json', 'r') as file:
            content = file.read()
        
            
      summary = summarize_changes(content)
      print(summary)