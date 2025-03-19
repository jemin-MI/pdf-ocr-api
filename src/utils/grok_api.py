import os

from groq import Groq

class GroqAPI:

    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def get_summary_using_groq(self, text: str,) -> str:
        try:
            if not text or len(text.strip()) < 10:
                return "Insufficient text for meaningful analysis."

            # Construct prompt
            prompt = f"""You are an experienced medical practitioner and radiologist.
            Analyze and summarize the following medical document.
            Maintain a professional tone and focus on key medical insights. 
            Provide a compact summary highlighting only the key medical insights, 
            important parameters, and any potential areas of concern: {text} """

            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                    }
                ],
                model="llama3-8b-8192",
                max_tokens=1024,
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error in AI summarization: {e}")
            # logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"

    def get_nutrient(self, summary):
        try:
            if not summary or len(summary.strip()) < 10:
                return "Insufficient text for meaningful analysis."

            # Construct prompt
            prompt = f""" You are an experienced medical practitioner.
                Analyze the following medical document summary.
                Provide a only High and Low Nutrient value list from it without any extra detail and data.
                Report Summary: {summary} """

            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                    }
                ],
                model="llama3-8b-8192",
                max_tokens=1024,
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error in AI summarization: {e}")
            # logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"

    def get_meal_plan(self, nutrient_summary, user_data = None ):
        try:
            if not nutrient_summary or len(nutrient_summary.strip()) < 10:
                return "Insufficient text for meaningful analysis."

            # Construct prompt
            prompt = f"""
            You are an experienced Nutrition Practitioner.  
            Analyze the following nutrient report and user profile details.  

            Based on the provided data, create a personalized **meal plan** and suggest **recipes** that align with the user's fitness goals, dietary preferences, and activity level.  

            **User Profile**  
            - **Age:** 40  
            - **Weight:** 100 kg  
            - **Height:** 160 cm  
            - **Gender:** Male  
            - **Fitness Goal:** Muscle Gain  
            - **Allergies:** None  
            - **Dietary Preferences:** Vegetarian  
            - **Activities:** Running, Swimming  
            - **Activity Level:** Sedentary  
            - **Meals Per Day:** 4  
            - **Plan Duration:** 3 Days  
            - **User ID:** 67d7c7011199f5701555a21e  

            **Nutrient Report Summary**  
            {nutrient_summary}  

            Ensure meals align with the user's **fitness goal** and **dietary preferences**.  
            """

            # Generate summary
            chat_completions = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": "Summary: "
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.7,
            )
            # Extract and return the summary text
            return chat_completions.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error in AI summarization: {e}")
            # logging.error(f"Error in AI summarization: {e}")
            return f"Error in AI analysis: {str(e)}"
