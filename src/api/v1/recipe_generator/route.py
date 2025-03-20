from fastapi import APIRouter, UploadFile, File, Query
from src.api.v1.recipe_generator.service import FileService, NutrientFinder

upload_router = APIRouter()


@upload_router.post("/get_summary_google")
def process_google(file: UploadFile = File(...)):
    return FileService.process_google(file)


@upload_router.post("/get_summary_groq")
def process_groq(file: UploadFile = File(...)):
    return FileService.process_groq(file)


@upload_router.post("/get_nutrients")
def process_groq(summary_text):
    return NutrientFinder.nutrient_finder(summary_text)


@upload_router.post("/get_meal_plan")
def process_groq(summary_text):
    return NutrientFinder.meal_planner(summary_text)


@upload_router.post("/generate_meal_plan")
def process_groq(file: UploadFile = File(...), mode: str = Query("groq", enum=["Google", "Groq"])):
    return NutrientFinder.meal_generator(file, mode)
