from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import (
    create_skill,
    delete_skill,
    get_skill_by_id,
    get_skill_by_name,
    get_skills
)
from app.db import get_db
from app.schemas.skill import SkillCreate, SkillRead


router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill_endpoint(skill_data: SkillCreate, db: Session = Depends(get_db)):
    existing_skill = get_skill_by_name(db, skill_data.name)
    if existing_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill with this name already exists"
        )

    return create_skill(db, skill_data)


@router.get("/", response_model=list[SkillRead])
def get_skills_endpoint(db: Session = Depends(get_db)):
    return get_skills(db)


@router.get("/{skill_id}", response_model=SkillRead)
def get_skill_endpoint(skill_id: int, db: Session = Depends(get_db)):
    skill = get_skill_by_id(db, skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill_endpoint(skill_id: int, db: Session = Depends(get_db)):
    skill = get_skill_by_id(db, skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    delete_skill(db, skill)