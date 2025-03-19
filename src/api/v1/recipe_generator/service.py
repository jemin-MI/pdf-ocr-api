from fastapi import HTTPException
from pathlib import Path
from src.utils.google_ocr import GoogleDocAI
from src.utils.grok_api import GroqAPI
from src.utils.helper import  get_text_from_file, save_text_file

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class FileService:
    @staticmethod
    def process_google(file):
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        if file:

            google_doc = GoogleDocAI()
            summary_text = google_doc.get_summary_using_google(file)

            save_text_file('groq_data', str(summary_text))

            print("The document contains the following text:-----------------------")
            print(summary_text)

            return {"filename": file.filename, "Summary": summary_text}


    @staticmethod
    def process_groq(file):
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        text = get_text_from_file(file.file)
        groq = GroqAPI()
        summary_text = groq.get_summary_using_groq(text)

        save_text_file('groq_data', summary_text)

        print("The document contains the following text:-----------------------")
        print(summary_text)

        return {"Summary": summary_text}


class NutrientFinder:

    @staticmethod
    def meal_planner(summary):
        if summary:
            groq = GroqAPI()
            result = groq.get_meal_plan(summary, user_data = None )
            return {"Nutrient": result}

    @staticmethod
    def nutrient_finder(summary):
        if summary:
            groq = GroqAPI()
            result = groq.get_nutrient(summary )
            return {"Nutrient": result}

    @staticmethod
    def meal_generator(file, mode):
        if file and mode:
            if mode == 'Google':
                file_summary = FileService.process_google(file)
            elif mode == 'Groq':
                file_summary = FileService.process_groq(file)
            nutrient_value = NutrientFinder.nutrient_finder(str(file_summary))
            meal_plan = NutrientFinder.meal_planner(str(nutrient_value))

            return {'Meal Plan': meal_plan}



