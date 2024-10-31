from fastapi import FastAPI, HTTPException
from banco_de_dados import banco_de_dados
from pydantic import BaseModel
import pyodbc


app = FastAPI()


class Dados(BaseModel):
    data: str
    hora: str
    tipo: str
    ordem: str
    descricao: str
    equipamento: str

@app.get("/")
def read_root():
    return {"It's": "Working"}

@app.post("/database")
def post_data(dados: Dados):
    db = banco_de_dados()
    db.criar_tabela_caso_nao_exista()
    insert = db.inserir_dados(dados)
    if insert == 1:
        return "Sucess"
    return str(insert)

@app.get("/database/last_row")
def get_last_Row():
    db = banco_de_dados()
    response = db.obter_ultimo_registro()
    return {"hora": str(response[1]), "data": str(response[0])} 

@app.get("/database")
def retrieve_ocorrencias():
    db = banco_de_dados()
    try: 
        response = db.obter_registros()
        response_of_route = [
            {
                "id": str(item[0]),
                "data": str(item[1]),
                "hora": str(item[2]),
                "tipo": str(item[3]),
                "ordem": str(item[4]),
                "descricao": str(item[5])
            }
            for item in response
        ]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"{str(Exception)}")

    return response_of_route
