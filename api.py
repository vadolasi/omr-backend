import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import aiofiles
import aioshutil
import msgspec
from brotli_asgi import BrotliMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

# from .main import entry_point_for_args

encoder = msgspec.json.Encoder()


class MsgSpecMsgPackResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return encoder.encode(content)


app = FastAPI(default_response_class=MsgSpecMsgPackResponse)
app.add_middleware(BrotliMiddleware)

dict_re = re.compile(r"'(q\d+)'\s*:\s*'(\w*)'")


def get_answers(content: str) -> dict[str, str]:
    answers = {}

    for match in re.finditer(dict_re, content):
        answers[match.group(1)] = match.group(2)

    return answers


avaliation = {
    "questions": {
        "1": "A",
        "2": "B",
        "3": "C",
        "4": "D",
        "5": "E",
        "6": "A",
        "7": "B",
        "8": "C",
        "9": "D",
        "10": "E",
        "11": "A",
        "12": "B",
        "13": "C",
        "14": "D",
        "15": "E",
        "16": "A",
        "17": "B",
        "18": "C",
        "19": "D",
        "20": "E",
        "21": "A",
        "22": "B",
        "23": "C",
        "24": "D",
        "25": "E",
        "26": "A",
        "27": "B",
        "28": "C",
        "29": "D",
        "30": "E",
        "31": "A",
        "32": "B",
        "33": "C",
        "34": "D",
        "35": "E",
        "36": "A",
        "37": "B",
        "38": "C",
        "39": "D",
        "40": "E",
    }
}


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/")
async def upload_file(
    file: UploadFile = File(...)
):
    async with aiofiles.tempfile.TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)

        await aioshutil.copytree("base", tempdir, dirs_exist_ok=True)

        async with aiofiles.open(
            tempdir / "MobileCamera" / file.filename,
            "wb",
        ) as out_file:
            content = await file.read()
            await out_file.write(content)

        result = subprocess.run(
            [sys.executable, "main.py", "-i", str(tempdir), "-a"],
            capture_output=True,
            text=True,
        )

        try:
            result.check_returncode()
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.stderr}

        answers = get_answers(result.stdout)

        data = {}

        for key, value in answers.items():
            question = key.replace("q", "")

            data[question] = {
                "response": value,
                "correct": avaliation["questions"][question],
            }
        
        return data


@app.post("/login")
async def login(username: str, password: str):
    if username == "admin" and password == "admin":
        return {"status": "success"}
    else:
        return {"status": "failure"}


@app.get("/avaliations")
async def get_avaliations():
    return [
        {"id": 1, "name": "Avaliação 1"},
        {"id": 2, "name": "Avaliação 2"},
        {"id": 3, "name": "Avaliação 3"},
    ]


@app.get("/avaliations/{avaliations_id}")
async def get_avaliations(avaliations_id: int):
    return {"id": avaliations_id, "name": f"Avaliação {avaliations_id}"}


@app.post("/avaliations/{avaliations_id}/{student_id}/answers")
async def post_avaliations(
    avaliations_id: int, student_id: int, answers: dict[str, str]
):
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
