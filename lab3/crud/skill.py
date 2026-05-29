from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreate


def get_skill_by_id(db: Session, skill_id: int) -> Skill | None:
    return db.query(Skill).filter(Skill.id == skill_id).first()


def get_skill_by_name(db: Session, name: str) -> Skill | None:
    return db.query(Skill).filter(Skill.name == name).first()


def get_skills(db: Session) -> list[Skill]:
    return db.query(Skill).all()


def create_skill(db: Session, skill_data: SkillCreate) -> Skill:
    skill = Skill(name=skill_data.name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill: Skill) -> None:
    db.delete(skill)
    db.commit()