import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from langchain_ollama import OllamaLLM


# LOCAL AI MODEL
llm = OllamaLLM(model="phi3")


movie_ids = [
    "tt0111161",
    "tt0468569",
    "tt1375666",
    "tt0816692"
]


reviews = []


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)


# OPEN FIRST PAGE
url = f"https://www.imdb.com/title/{movie_ids[0]}/reviews"

driver.get(url)

print("\nSIGN INTO IMDb MANUALLY IN CHROME")
print("After signing in, press ENTER here")

input()


for movie_id in movie_ids:

    url = f"https://www.imdb.com/title/{movie_id}/reviews"

    print("\nOpening:", url)

    driver.get(url)

    time.sleep(8)


    # LOAD MORE REVIEWS
    for i in range(5):

        try:

            button = driver.find_element(
                By.CSS_SELECTOR,
                "button.ipc-see-more__button"
            )

            driver.execute_script(
                "arguments[0].click();",
                button
            )

            print("Loaded more reviews")

            time.sleep(3)

        except:
            break


    # REVIEW BLOCKS
    elements = driver.find_elements(
        By.CSS_SELECTOR,
        '[data-testid="review-overflow"]'
    )

    print("Reviews found:", len(elements))


    for e in elements:

        try:

            text = e.text.strip()

            if len(text) > 80:

                prompt = f"""
                Classify sentiment as:

                Positive
                Negative
                Neutral

                Review:
                {text}

                Answer ONLY one word.
                """

                sentiment = llm.invoke(prompt)

                reviews.append({
                    "review": text,
                    "sentiment": sentiment.strip(),
                    "source": "IMDb"
                })

                print("Added review")

        except:
            continue


driver.quit()


df = pd.DataFrame(reviews)

df.drop_duplicates(inplace=True)

df.to_csv(
    "imdb_real_reviews.csv",
    index=False
)

print("\nDataset generated!")
print("Total reviews:", len(df))