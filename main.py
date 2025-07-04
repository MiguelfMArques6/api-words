from fastapi import FastAPI, UploadFile, HTTPException
import pandas as pd
import io

app = FastAPI()

@app.post("/conta-palavras/")
async def conta_palavras(ficheiro: UploadFile, coluna: str):
    try:
        conteudo = await ficheiro.read()
        df = pd.read_csv(io.BytesIO(conteudo))
        
        if coluna not in df.columns:
            raise HTTPException(status_code=400, detail=f"A coluna '{coluna}' não existe no ficheiro.")
        
        total_palavras = df[coluna].astype(str).str.split().str.len().sum()
        
        return {"total_palavras": int(total_palavras)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
