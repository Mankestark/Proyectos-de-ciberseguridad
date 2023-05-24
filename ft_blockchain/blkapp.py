#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Dict, List


from pydantic import BaseModel

from blockchain import Blockchain

blockchain = Blockchain()

app = FastAPI(
    title='FT_BLOCKCHAINS',
    description='Rest API for BlockChains',
    version='1.0.0'
)


class Transaction(BaseModel):
    sender: str
    recipient: str
    amount: float


@app.get('/', tags=['Inicio'])
def raiz() -> HTMLResponse:
    html_contenido = '''
    <html>
        <head>
            <title>API ft_Blockchains</title>
        </head>
        <body>
            <h1>Rest API for ft_BlockChains</h1>
            <p>
            <h3>Para gestionar la API abra la URL:
            <a href="http://127.0.0.1:8000/docs/">http://127.0.0.1/[puerto]/docs</a></h3>
            El puerto normalmente es el: <i>8000</i>
            </p>
            42 Málaga
        </body>
    </html>
    '''
    return HTMLResponse(html_contenido, status_code=200)


# Informacion sobre cadena de bloques
@app.get('/chain', tags=['BlockChain'], status_code=200)
def chain() -> JSONResponse:
    # return blockchain.chain
    return JSONResponse(content=blockchain.chain, status_code=200)


@app.get('/chain/nchains', tags=['BlockChain'])
def chain() -> JSONResponse:
    return JSONResponse(content={'nchains': len(blockchain.chain)}, status_code=200)


@app.get('/chain/', tags=['BlockChain'], response_model=dict, status_code=200)
def chain() -> JSONResponse:
    return JSONResponse(content=blockchain.chain[-1])


@app.get('/mine/', tags=['BlockChain'], status_code=200)
def mine() -> dict:
    return JSONResponse(content=blockchain.new_block(), status_code=200)


@app.get('/transactions', tags=['BlockChain'], status_code=200)
def showtransaction() -> dict:
    if len(blockchain.current_transactions):
        return JSONResponse(content=blockchain.current_transactions, status_code=200)
    return JSONResponse(content={}, status_code=200)


@app.get('/transactions/', tags=['BlockChain'])
def showtransaction() -> dict:
    if len(blockchain.current_transactions):
        return JSONResponse(content=blockchain.current_transactions[-1], status_code=200)
    return JSONResponse(content={}, status_code=200)


# Envia una nueva transacción para enviar al bloque.
@app.post('/transactions/new', tags=['BlockChain'], response_model=dict, status_code=201)
def newtransaction(transaction: Transaction) -> dict:
    return JSONResponse(blockchain.new_transaction(transaction.sender,
                                      transaction.recipient,
                                      transaction.amount), status_code=201)


@app.get('/validate/', tags=['BlockChain'])
def validate() -> dict:
    pass
