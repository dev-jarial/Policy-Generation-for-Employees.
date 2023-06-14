import docx
import openai
from fastapi import FastAPI

# Set your OpenAI API key
openai.api_key = "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"

app = FastAPI()

def generate_completion(api_key, conversation_history, max_tokens=7200):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            *[
                {"role": "user", "content": msg}
                for msg in conversation_history
            ],
        ],
        max_tokens=max_tokens,
        n=1,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def generate_document(conversation_history):
    document = docx.Document()
    completion = generate_completion(openai.api_key, conversation_history)
    document.add_paragraph(completion)
    document.save("prompt_completion.docx")

@app.post("/generate_prompt")
def generate_prompt(company_name: str, company_details: str, employee_name: str, date: str, your_name: str, your_title: str):
    with open("policy.txt", "r") as file:
        policy_text = file.read()

    conversation_history = [
        f"Company Name: {company_name}",
        f"Company Details: {company_details}",
        f"Employee Name: {employee_name}",
        f"[Date]: {date}",
        f"[Your Name]: {your_name}",
        f"[Your Title]: {your_title}",
        policy_text
    ]
    generate_document(conversation_history)
    return {"message": "Prompt completion generated and saved as prompt_completion.docx"}
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
