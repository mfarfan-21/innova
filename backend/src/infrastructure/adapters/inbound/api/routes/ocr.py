"""
Rutas API para OCR de matrículas
"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
from application.services.ocr_service import OCRService
from infrastructure.adapters.outbound.file.plates_dat_repository import PlatesDatRepository
from presentation.dto.ocr_dto import (
    OCRRequest, OCRResponseSimple, OCRResponseDetailed,
    OCRErrorResponse, CharacterDTO, PlateCoordinatesDTO
)

router = APIRouter(prefix="/ocr", tags=["OCR"])

# Paths: backend/src/... -> backend/assets/
BASE_DIR = Path(__file__).parent.parent.parent.parent.parent.parent.parent
PLATES_DAT_PATH = BASE_DIR / "assets" / "plates.dat"
IMAGES_PATH = BASE_DIR / "assets" / "imgs"

plate_repository = PlatesDatRepository(str(PLATES_DAT_PATH))
ocr_service = OCRService(plate_repository)


@router.post("/recognize", response_model=OCRResponseSimple, responses={404: {"model": OCRErrorResponse}})
async def recognize_plate(request: OCRRequest):
    """Reconoce la matrícula en una imagen (solo número de placa)"""
    try:
        plate = ocr_service.recognize_plate(request.image_name)
        
        if plate is None:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró información OCR para: {request.image_name}"
            )
        
        return OCRResponseSimple(
            plate_number=plate.plate_number,
            image_name=plate.image_name
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.post("/recognize/detailed", response_model=OCRResponseDetailed, responses={404: {"model": OCRErrorResponse}})
async def recognize_plate_detailed(request: OCRRequest):
    """Reconoce matrícula con información detallada (coordenadas, caracteres, metadatos)"""
    try:
        plate = ocr_service.recognize_plate(request.image_name)
        
        if plate is None:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró información OCR para: {request.image_name}"
            )
        
        characters_dto = [
            CharacterDTO(char=c.char, left=c.left, top=c.top, width=c.width, height=c.height)
            for c in plate.characters
        ]
        
        coordinates_dto = PlateCoordinatesDTO(
            top_left=plate.coordinates.top_left,
            top_right=plate.coordinates.top_right,
            bottom_right=plate.coordinates.bottom_right,
            bottom_left=plate.coordinates.bottom_left
        )
        
        return OCRResponseDetailed(
            plate_number=plate.plate_number,
            image_name=plate.image_name,
            num_characters=plate.num_characters,
            num_plates_in_image=plate.num_plates_in_image,
            characters=characters_dto,
            coordinates=coordinates_dto,
            is_valid=plate.is_valid()
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/exists/{image_name}", response_model=dict)
async def check_image_exists(image_name: str):
    """Verifica si existe información OCR para una imagen"""
    exists = ocr_service.image_exists(image_name)
    return {"image_name": image_name, "exists": exists}


@router.get("/plates", response_model=dict)
async def list_all_plates(limit: int = Query(default=None, ge=1, le=10000)):
    """Lista matrículas disponibles (solo imágenes que existen en servidor)"""
    all_plates = ocr_service.get_all_plates()
    
    available_plates = []
    for plate in all_plates:
        image_path = IMAGES_PATH / plate.image_name
        if image_path.exists():
            available_plates.append(plate)
            if limit is not None and len(available_plates) >= limit:
                break
    
    return {
        "total": len(all_plates),
        "available": len(available_plates),
        "showing": len(available_plates),
        "plates": [
            {
                "image_name": p.image_name,
                "plate_number": p.plate_number,
                "num_characters": p.num_characters
            }
            for p in available_plates
        ]
    }


@router.get("/image/{image_name}")
async def get_plate_image(image_name: str):
    """Sirve imagen de matrícula"""
    image_path = IMAGES_PATH / image_name
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail=f"Imagen no encontrada: {image_name}")
    
    return FileResponse(image_path)
