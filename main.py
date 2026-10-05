from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# O título aparecerá na documentação automática
app = FastAPI(title="API Smart Home - Clima")

# Banco de dados em memória
banco_em_memoria = []


# Modelo de Dados (Contrato estrito via Pydantic)
# Isso substitui toda a validação manual de 'if' que fazíamos no Flask
class LeituraClima(BaseModel):
    id: str
    temperatura: float


@app.post("/sensores/clima", status_code=201)
async def registrar_leitura(leitura: LeituraClima):
    # O FastAPI já garantiu que 'id' é string e 'temperatura' é float.
    # Se o cliente enviar um JSON errado, o FastAPI retorna Erro 422 automaticamente.
    banco_em_memoria.append(leitura.model_dump())  # Converte o objeto para dicionário

    return {"mensagem": "Leitura registrada com sucesso!", "dados": leitura}


@app.get("/sensores/clima")
async def listar_todos():
    return {"total_registros": len(banco_em_memoria), "leituras": banco_em_memoria}


# Note a tipagem do parâmetro da rota (sensor_id: str)
@app.get("/sensores/clima/{sensor_id}")
async def buscar_por_id(sensor_id: str):
    for leitura in banco_em_memoria:
        if leitura['id'] == sensor_id:
            return leitura

    # O HTTPException substitui o retorno manual de tuplas (jsonify, 404) do Flask
    raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' não encontrado.")


@app.delete("/sensores/clima/{sensor_id}")
async def deletar_sensor(sensor_id: str):
    global banco_em_memoria
    tamanho_original = len(banco_em_memoria)

    banco_em_memoria = [l for l in banco_em_memoria if l['id'] != sensor_id]

    if len(banco_em_memoria) < tamanho_original:
        return {"mensagem": f"Sensor '{sensor_id}' removido com sucesso."}

    raise HTTPException(status_code=404, detail=f"Sensor '{sensor_id}' não encontrado para exclusão.")