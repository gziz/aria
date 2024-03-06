from . import database, schemas, models
from .agent import OpenAIClient
from sqlalchemy.orm import Session
from pydantic import ValidationError, TypeAdapter
from fastapi import Depends, FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = OpenAIClient()
    yield

app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(database.engine)

QuestionAdapter = TypeAdapter(schemas.Question)


@app.get('/')
def index(db: Session = Depends(database.get_db)):
    from sqlalchemy.sql import text
    result = db.execute(text("SELECT * FROM questions;"))
    print(result.fetchone())

    return "Hi there!"


@app.post('/question')
async def receive_question(request: Request, db: Session = Depends(database.get_db)):
    try:
        data = await request.json()

        msg = await validate_data(data)
        ai_text_answer = await send_message(msg)
        print("ai_text_answer", ai_text_answer)
        question = QuestionAdapter.validate_python(
            {"question": msg.text, "answer": ai_text_answer})
        await save_to_db(obj=question, db=db)
        return {"answer": ai_text_answer}

    except ValidationError as e:
        return {"status": "error"}


async def validate_data(data) -> schemas.Message:
    try:
        msg = schemas.Message(**data["message"])
        return msg
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="Invalid data.")


async def send_message(msg: schemas.Message) -> str:
    """Call OpenAI and reply to user"""

    response = app.state.agent.send_message(msg)
    ai_text_answer = response.choices[0].message.content

    return ai_text_answer


async def save_to_db(obj: schemas.Question, db: Session = Depends(database.get_db)):
    record = models.Question(question=obj.question, answer=obj.answer)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
