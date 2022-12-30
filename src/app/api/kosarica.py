from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.api.models import KosaricaDB, KosaricaSchema

router = APIRouter()


@router.post("/", response_model=KosaricaDB, status_code=201)
async def create_kosarica(payload: KosaricaSchema):
    kosarica_id = await crud.post(payload)

    response_object = {
        "id": kosarica_id,
        "imeKosarice": payload.imeKosarice,
        "seznamTrgovin": payload.seznamTrgovin,
    }

    return response_object


@router.get("/{id}/", response_model=KosaricaDB)
async def read_kosarica(id: int = Path(..., gt=0),):
    kosarica = await crud.get(id)
    if not kosarica:
        raise HTTPException(status_code=404, detail="Kosarica ni bila najdena")
    return kosarica


@router.get("/", response_model=List[KosaricaDB])
async def read_all_kosarice():
    return await crud.get_all()


@router.put("/{id}/", response_model=KosaricaDB)
async def posodobi_kosarico(payload: KosaricaSchema, id: int = Path(..., gt=0),):
    kosarica = await crud.get(id)
    if not kosarica:
        raise HTTPException(status_code=404, detail="Kosarica ni bila najdena.")

    kosarica_id = await crud.put(id, payload)

    response_object = {
        "id": kosarica_id,
        "imeKosarice": payload.imeKosarice,
        "seznamTrgovin": payload.seznamTrgovin,
    }
    return response_object


@router.delete("/{id}/", response_model=KosaricaDB)
async def delete_kosarica(id: int = Path(..., gt=0)):
    kosarica = await crud.get(id)
    if not kosarica:
        raise HTTPException(status_code=404, detail="Kosarica ni bila najdena.")

    await crud.delete(id)

    return kosarica
