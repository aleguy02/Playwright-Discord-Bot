import os
from dotenv import load_dotenv
from groq import Groq

def create_summary(article_data: dict):
    load_dotenv()

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": "You will be provided a news article's headline delimited in square braces and its article content delimited in parentheses. Follow the following set of instructions.\n1. Read the headline carefully. You should not output anything. The point of this step is for you to try to get an idea of what the article's content will be about.\n2. Read the following article critically, maintaining an unbiased and impartial perspective. Identify and extract key ideas, including significant words, numbers, names, and dates. Your goal is to create a framework that will allow you to write a concise summary of the article and a list of key political terms and concepts. Internally develop a chain of thought on how to summarize the article effectively. Do not output anything. \n3.  Write a summary of the article in one paragraph, limited to 7 sentences or less. This summary should capture the main ideas clearly and concisely. Create a list of key political terms and concepts relevant to the article. This list should include definitions or explanations tailored for individuals who may not be familiar with political jargon, aiming to enhance their understanding and confidence in interpreting political discussions."
            },
            {
                "role": "assistant",
                "content": "I'm ready to follow the instructions. Please provide the news article's headline and content. I'll perform the three steps and write the two paragraphs accordingly."
            },
            {
                "role": "user",
                "content": f"[{article_data["headline"]}]\n({article_data["article"]})"
            }
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None,
    )

    summary = ""
    summary = "".join(chunk.choices[0].delta.content or "" for chunk in completion)


    return summary