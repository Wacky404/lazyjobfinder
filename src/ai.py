from openai import OpenAI
from dotenv import load_dotenv
from src.utils.logger import logger
from typing import Optional
import os

load_dotenv()
CLIENT = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    # if you are using LITEllM for proxy server: https://docs.litellm.ai/docs/proxy/user_keys
    # base_url=os.getenv("BASE_URL")
)
logger.debug(f"Client has been iniated.")


def ai_cmp(prompt: str, model: str = 'gpt-4o-mini-2024-07-18', role_content: Optional[str] = None) -> str:
    if role_content is None:
        role_content = '''
        > You are an expert career evaluation assistant trained to compare candidate resumes to job descriptions and job titles.
        >
        > Your primary function is to analyze how well a candidate’s background (including work experience, education, and personal projects) aligns with a job’s requirements or expectations.
        >
        > You always respond with:
        > 1. A **similarity score between 0.0 and 1.0**, where:
        >    - `1.0` = Perfect match
        >    - `0.0` = No match at all
        >    - Values in between represent partial fit
        > 2. A **brief justification in bullet point form** (2–4 bullets max) explaining your reasoning
        >
        > Additional Instructions:
        > - Be concise, neutral, and objective in your evaluation.
        > - Do not summarize the input unless it helps support your score.
        > - You may infer implied responsibilities and skills from job titles when no description is provided.
        > - When comparing resumes to job descriptions, focus only on **relevant overlap**, not general resume quality.
        > - If no matching content is found, assign a score of `0.0` and state clearly that there is no alignment.
        >
        > You will be provided with one of the following inputs:
        > - **Work Experience** vs. **Job Description**
        > - **Education** vs. **Education Requirements**
        > - **Projects** vs. **Job Title**
        >
        > Your output must always follow this structure:
        >
        > ```
        > Score: X.XX
        > Justification:
        > - [Bullet point 1]
        > - [Bullet point 2]
        > - [Bullet point 3]
        > ```
        >
        > Be strict, fair, and consistent in your scoring.
        '''
        logger.debug("Default role content has been set.")

    completion = CLIENT.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": role_content},
            {"role": "user", "content": prompt}
        ]
    )

    logger.debug(f"Completion is done, with prompt:\n{prompt}")
    logger.debug(f"Response:\n{completion.choices[0].message}")
    return completion.choices[0].message.content


if __name__ == '__main__':
    print(ai_cmp(prompt="Hello, what are you doing right now?"))
