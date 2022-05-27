from fastapi import FastAPI
from pydantic import BaseModel
import paraphrasingModule
import uvicorn

paraphraser = paraphrasingModule.PegasusParaphraser()

class Paragraph(BaseModel):
    paragraph: str

# For testing("Link"/paraphrase)the JSON Example below:
# {
#     "paragraph": "input text"
# }

app = FastAPI()


@app.get("/")
def get_root():
    return "This is the Text Paraphrasing Tool"


@app.post("/paraphrase")
async def paraphrase_text(text: Paragraph):
    paraphrased_text = paraphraser.paraphrase_text(text.paragraph)

    return {
        "original": text.paragraph,
        "paraphrased": paraphrased_text,

    }

if __name__ == "__main__":
    uvicorn.run(app)
