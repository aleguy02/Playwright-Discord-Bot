# Need to figure out how to merge branch

import os
from dotenv import load_dotenv
from groq import Groq

def create_summary(article_data: dict):
    load_dotenv()

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )
    chat_completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": ("You are now an assistant whose goal to make political discussions more accessible to readers, especially those who are not familiar with political jargon. "
                            "You will be provided a news article's headline delimited in square braces and its article content delimited in parentheses. Please create a concise summary of the article and a list of key political terms, simplifying the language to help build the reader’s confidence in understanding political topics. "
                            "**Constraints**: "
                            "1. **Unbiased Analysis**: You must analyze the article critically, without showing bias toward any political ideology. Your summary and key terms should be neutral and fact-based. "
                            "2. **Focus on Key Information**: When processing the article, identify the most important points, including: "
                            "- Major events or actions described "
                            "- Names of key individuals or organizations "
                            "- Dates or timelines "
                            "- Important political terms and concepts "
                            "3. **Summary**: After reading the article, write a concise, 1-paragraph summary of the main ideas. The summary should be neutral, clear, and provide an overview of the political issue or event discussed in the article. "
                            "4. **Key Terms**: Identify 7 political terms or concepts that are central to the article. Identify and extract key ideas, including significant words, numbers, names, and dates. For each term, write a brief explanation that will help readers unfamiliar with political jargon understand the concept. Each explanation should focus on breaking down the meaning in an accessible way. "
                            "5. **Format**: The summary and key terms should be provided in JSON format, structured as follows: "
                            '{"summary": "Your 1-paragraph summary here", "key_terms": [{"term": "Political Term 1", "explanation": "Simplified explanation of the term."}, {"term": "Political Term 2", "explanation": "Simplified explanation of the term."}, {"term": "Political Term 3", "explanation": "Simplified explanation of the term."}, {"term": "Political Term 4", "explanation": "Simplified explanation of the term."}, {"term": "Political Term 5", "explanation": "Simplified explanation of the term."}, {"term": "Political Term 6", "explanation": "Simplified explanation of the term."}, {"term": "Political Term 7", "explanation": "Simplified explanation of the term."}]}'
                            "IMPORTANT: REMEMBER YOUR RESPONS IS A STRINGIFIED JSON. DO NOT RESPOND IN ANY OTHER FORMAT. IF YOU ARE UNABLE TO FILL ANY OF THE FIELDS, PUT \"MISSING\" IN THE PLACE OF THE FIELDS CONTENT. "
                            f"Here is the article's headline and contents: [{article_data["headline"]}], ({article_data["article"]})")
            }
        ],
        temperature=0.4,
        max_tokens=2048,
        top_p=1,
        stream=False,
        stop=None,
    )

    return chat_completion.choices[0].message.content