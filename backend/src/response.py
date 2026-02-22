from transformers import pipeline, AutoConfig
from huggingface_hub import InferenceClient
import io
import base64
from PIL import Image
import os
import time
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

def generate_response(input_img, query, using_local_model, chat_history):

    #streamlit input to PIL image
    img = Image.open(input_img)

    #Changing the PIL image to bytes so we can pass it into the message
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_as_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')

    response = ""

    if(using_local_model):
        print("LOCAL")
        start_time = time.time()

        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": f"Here is the conversation so far: {chat_history}. Continue the conversation naturally. \n Provide responses without using special formatting, while still being descriptive."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": f"data:image/png;base64,{img_as_bytes}"},
                    {"type": "text", "text": query}
                ]
            }
        ]

        AutoConfig.from_pretrained(
            "google/gemma-3-4b-it",
            token=HF_TOKEN
        )
        
        pipe = pipeline(
            "image-text-to-text",
            model="google/gemma-3-4b-it",
            )

        output = pipe(messages, max_new_tokens=200)

        response = output[0]["generated_text"][-1]["content"]
        run_time = time.time() - start_time
        print(f"Local response took {run_time} seconds")

    else:
        print("API")
        start_time = time.time()

        messages=[
            {
                "role": "system", 
                "content": [{"type": "text", "text": f"Here is the conversation so far: {chat_history}. Continue the conversation naturally. \n Provide responses without using special formatting, while still being descriptive."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_as_bytes}"}}
                ],
            }
        ]
        client = InferenceClient(token=HF_TOKEN)

        completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:featherless-ai",
            messages=messages,
            max_tokens=500
        )
        
        run_time = time.time() - start_time
        print(f"API response took {run_time} seconds")

        response = completion.choices[0].message.content

    return response

