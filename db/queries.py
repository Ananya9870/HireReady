from .connection import ResumeRecord

def save_resume(db, user_id, content, filename="tailored_resume.pdf"):
    db_resume = ResumeRecord(filename=filename, content=content)
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def delete_resume(db, resume_id=None, list_only=False):
    if list_only:
        return db.query(ResumeRecord).all()
    
    item = db.query(ResumeRecord).filter(ResumeRecord.id == resume_id).first()
    if item:
        db.delete(item)
        db.commit()
    return None