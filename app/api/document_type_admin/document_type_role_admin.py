from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.document_type_role import DocumentTypeRole

from app.schemas.document_type_role import (
    DocumentTypeRoleCreate,
    DocumentTypeRoleUpdate,
    DocumentTypeRoleResponse
)

router = APIRouter(
    prefix="/admin/document-type-roles",
    tags=["Admin - Document Type Roles"]
)


@router.get("", response_model=list[DocumentTypeRoleResponse])
def get_all_document_type_roles(
    db: Session = Depends(get_db)
):
    return db.query(DocumentTypeRole).all()


@router.get("/{id}", response_model=DocumentTypeRoleResponse)
def get_document_type_role(
    id: UUID,
    db: Session = Depends(get_db)
):
    role = (
        db.query(DocumentTypeRole)
        .filter(DocumentTypeRole.id == id)
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Document type role not found"
        )

    return role


@router.post("", response_model=DocumentTypeRoleResponse)
def create_document_type_role(
    payload: DocumentTypeRoleCreate,
    db: Session = Depends(get_db)
):
    exists = (
        db.query(DocumentTypeRole)
        .filter(
            (DocumentTypeRole.name == payload.name) |
            (DocumentTypeRole.code == payload.code)
        )
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Document type role already exists"
        )

    role = DocumentTypeRole(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        role_level=payload.role_level,
        is_predefined=payload.is_predefined,
        is_active=payload.is_active
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


@router.put("/{id}", response_model=DocumentTypeRoleResponse)
def update_document_type_role(
    id: UUID,
    payload: DocumentTypeRoleUpdate,
    db: Session = Depends(get_db)
):
    role = (
        db.query(DocumentTypeRole)
        .filter(DocumentTypeRole.id == id)
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Document type role not found"
        )

    if role.is_predefined:
        raise HTTPException(
            status_code=403,
            detail="Predefined document type roles cannot be modified"
        )

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(role, field, value)

    db.commit()
    db.refresh(role)

    return role


@router.delete("/{id}")
def delete_document_type_role(
    id: UUID,
    db: Session = Depends(get_db)
):
    role = (
        db.query(DocumentTypeRole)
        .filter(DocumentTypeRole.id == id)
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=404,
            detail="Document type role not found"
        )

    if role.is_predefined:
        raise HTTPException(
            status_code=403,
            detail="Predefined document type roles cannot be deleted"
        )

    role.is_active = False
    db.commit()

    return {"message": "Document type role deleted successfully"}
