import json

from typing import List, Union
from fastapi import FastAPI, UploadFile, HTTPException, status


app = FastAPI()


def to_camel_case(string: str) -> str:
    string = string.strip()

    sep = None

    if "_" in string: sep = "_"
    elif "-" in string: sep = "-"
    elif " " in string: sep = " "

    if sep is None:
        return string[0].lower() + "".join(word for word in string[1:])

    strings = string.split(sep)

    return strings[0].lower() + "".join(word.capitalize() for word in strings[1:])


def check_file_extension(filename: str, allowed_extensions: List[str]) -> None:
    extension = filename.split('.')[-1]
    if extension not in allowed_extensions:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@app.post("/api/fileHandler/")
def file_handler(file: UploadFile):
    check_file_extension(filename=file.filename, allowed_extensions=['json'])

    data = json.loads(file.file.read())
    formatted_data = list()

    for row in data:
        formatted_row = dict()
        for key, value in row.items():
            formatted_key = to_camel_case(string=key)
            formatted_row[formatted_key] = value

        if any(key in ["", None] for key in formatted_row.keys()): continue
        formatted_data.append(formatted_row)
    
    return formatted_data
