from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# jinja2 Template 생성. 인자로 directory 입력
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    name: str
    price: float

# response_class=HTMLResponse를 생략하면 application/json으로 Swagger UI에서 인식(별 문제는 없음)
@app.get("/items/{item_id}", response_class=HTMLResponse)
# template engine을 사용할 경우 반드시 Request 객체가 인자로 입력되어야 함. 
async def read_item(request: Request, item_id: str, q: str | None = None):
    # 내부에서 pydantic 객체 생성. 
    item = Item(
        name="test_item", 
        price=1000.0
    )
    # pydantic model값을 dict 변환. 
    item_dict = item.model_dump()
    
    return templates.TemplateResponse(
        request=request, 
        name="item.html", 
        context={"item_id": item_id, "q_str": q, "item": item, "item_dict": item_dict}
    )


