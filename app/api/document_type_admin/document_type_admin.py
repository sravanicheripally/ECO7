from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.document_type import DocumentType
from app.schemas.document_type import (
    DocumentTypeCreate,
    DocumentTypeUpdate,
    DocumentTypeResponse
)

router = APIRouter(
    prefix="/admin/document-types",
    tags=["Admin - Document Types"]
)


@router.get("", response_model=list[DocumentTypeResponse])
def get_all_document_types(
    db: Session = Depends(get_db)
):
    return db.query(DocumentType).all()


@router.get("/{id}", response_model=DocumentTypeResponse)
def get_document_type(
    id: UUID,
    db: Session = Depends(get_db)
):
    doc_type = (
        db.query(DocumentType)
        .filter(DocumentType.id == id)
        .first()
    )

    if not doc_type:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )

    return doc_type


@router.post("", response_model=DocumentTypeResponse)
def create_document_type(
    payload: DocumentTypeCreate,
    db: Session = Depends(get_db)
):
    exists = (
        db.query(DocumentType)
        .filter(DocumentType.code == payload.code)
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Document type already exists"
        )

    doc_type = DocumentType(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        icon=payload.icon,
        allowed_extensions=payload.allowed_extensions,
        max_file_size_mb=payload.max_file_size_mb,
        requires_approval=payload.requires_approval,
        is_active=payload.is_active,
        created_by=None,
        updated_by=None
    )

    db.add(doc_type)
    db.commit()
    db.refresh(doc_type)

    return doc_type


@router.put("/{id}", response_model=DocumentTypeResponse)
def update_document_type(
    id: UUID,
    payload: DocumentTypeUpdate,
    db: Session = Depends(get_db)
):
    doc_type = (
        db.query(DocumentType)
        .filter(DocumentType.id == id)
        .first()
    )

    if not doc_type:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(doc_type, field, value)

    doc_type.updated_by = None

    db.commit()
    db.refresh(doc_type)

    return doc_type


@router.delete("/{id}")
def delete_document_type(
    id: UUID,
    db: Session = Depends(get_db)
):
    doc_type = (
        db.query(DocumentType)
        .filter(DocumentType.id == id)
        .first()
    )

    if not doc_type:
        raise HTTPException(
            status_code=404,
            detail="Document type not found"
        )

    doc_type.is_active = False
    doc_type.updated_by = None

    db.commit()

    return {"message": "Document type deleted successfully"}
