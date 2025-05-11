# <form action="/login/" method="post">
#   <input name="username" />
#   <input name="password" type="password" />
#   <button type="submit">Login</button>
# </form>


from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    return {"message": f"Welcome back, {username}!"}



# You must call it using a form or curl/Postman with Content-Type: application/x-www-form-urlencoded



#####ABOVE AND THIS ONE ARE EXACTLY SAME BUT WRITTEN IN DIFF WAY
from typing import Annotated
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class LoginForm(BaseModel):
    username: str
    password: str

@app.post("/login/")
async def login(data: Annotated[LoginForm, Form()]):
    return {"message": f"Logged in as {data.username}"}
