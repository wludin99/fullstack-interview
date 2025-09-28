"""Data seeding script for German tender templates."""

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
import uuid


def seed_german_tender_templates():
    """Seed the database with German tender template data."""
    db = SessionLocal()
    
    try:
        # German Public Tender Checklist Template
        checklist_id = str(uuid.uuid4())
        checklist = Checklist(
            id=checklist_id,
            name="Deutsche Ausschreibung - Standard Checkliste",
            description="Standard-Checkliste für deutsche öffentliche Ausschreibungen"
        )
        db.add(checklist)
        
        # Questions for German tenders
        questions = [
            {
                "text": "Welche Art von Leistung wird ausgeschrieben?",
                "order_index": 1
            },
            {
                "text": "Welche Vergabeverfahren wird angewendet? (Offenes Verfahren, Nichtoffenes Verfahren, Verhandlungsverfahren)",
                "order_index": 2
            },
            {
                "text": "Welche Schwellenwerte gelten für diese Ausschreibung?",
                "order_index": 3
            },
            {
                "text": "Welche Nachweise sind für die Eignung erforderlich?",
                "order_index": 4
            },
            {
                "text": "Welche technischen Anforderungen werden gestellt?",
                "order_index": 5
            },
            {
                "text": "Welche Umwelt- und Nachhaltigkeitskriterien sind zu erfüllen?",
                "order_index": 6
            },
            {
                "text": "Welche Fristen und Termine sind zu beachten?",
                "order_index": 7
            },
            {
                "text": "Welche Vertragsbedingungen gelten?",
                "order_index": 8
            }
        ]
        
        for q_data in questions:
            question = Question(
                id=str(uuid.uuid4()),
                checklist_id=checklist_id,
                text=q_data["text"],
                order_index=q_data["order_index"]
            )
            db.add(question)
        
        # Conditions for German tenders
        conditions = [
            {
                "text": "Die Ausschreibung entspricht den Vorgaben der Vergabeverordnung (VgV)",
                "order_index": 1
            },
            {
                "text": "Alle erforderlichen Nachweise sind vollständig und gültig",
                "order_index": 2
            },
            {
                "text": "Die technischen Anforderungen sind erfüllt",
                "order_index": 3
            },
            {
                "text": "Die Umwelt- und Nachhaltigkeitskriterien sind erfüllt",
                "order_index": 4
            },
            {
                "text": "Die Fristen und Termine werden eingehalten",
                "order_index": 5
            },
            {
                "text": "Die Vertragsbedingungen sind akzeptabel",
                "order_index": 6
            }
        ]
        
        for c_data in conditions:
            condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=checklist_id,
                text=c_data["text"],
                order_index=c_data["order_index"]
            )
            db.add(condition)
        
        db.commit()
        print("German tender template data seeded successfully")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_german_tender_templates()
