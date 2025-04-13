import p2t_clustering as pc
import fitz

from openai import OpenAI
from config import *

class NovaNotes:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=API_KEY)
    
    def run_inference(self, image_path: str, scale_factor = 1) -> list[str]:
        latex_extract = pc.extract_latex_items(image_path)
        text_clusters = pc.cluster_p2t_output(latex_extract, scale_factor = scale_factor)

        prompts_list: list[str] = pc.clusters_to_text(text_clusters)

        return [self.__ask_gpt(prompt) for prompt in prompts_list]
    
    def __ask_gpt(self, prompt: str, answer_mode: str = True) -> str:
        if answer_mode:
            context = "This is formatted LaTeX code depicting some academic question. Answer in 150 words or less. Please answer and format your new answer in LaTeX code and continue the solving if unfinished."
        else:
            context = "Give me a one sentence question about this topic."
        try:
            chat = self.client.chat.completions.create(
                model      = DEFAULT_MODEL,
                messages   = [{"role": "system", "content": context}, {"role": "user", "content": prompt}],
                max_tokens = MAX_TOKENS
            )
            return chat.choices[0].message.content.strip()
        except Exception as e:
            print(f"API Error: {e}")
            return "Sorry, something went wrong when talking to OpenAI."
        
    def get_questions_with_file(self, file_path: str) -> str:
        text = self.extract_text_from_pdf(file_path)

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"Based on this PDF content, give me 10 questions in LaTeX code in one line split by the # symbol, and do not give any uncessary words that aren't part of the question.:\n\n{text[:10000]}"  # GPT input limit handling
                }
            ]
        )

        return response.choices[0].message.content
    
    def extract_text_from_pdf(self, path):
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])


        