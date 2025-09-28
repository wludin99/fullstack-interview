#!/usr/bin/env python3
"""
Seed script to populate the database with a comprehensive German tender checklist.
This script creates a detailed checklist with relevant questions and conditions
for analyzing German public tender documents.
"""

import sys
import os
import uuid
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database import get_db
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition

def create_german_tender_checklist():
    """Create a comprehensive German tender checklist."""
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create the main checklist
        checklist_id = str(uuid.uuid4())
        checklist = Checklist(
            id=checklist_id,
            name="Deutsche Ausschreibung - Vollständige Checkliste",
            description="Umfassende Checkliste für die Analyse deutscher öffentlicher Ausschreibungen. Deckt alle wichtigen Aspekte von Vergabeverfahren ab.",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(checklist)
        
        # Questions for German tender analysis
        questions = [
            {
                "text": "Was ist der Abgabetermin für die Teilnahmeanträge?",
                "order_index": 1
            },
            {
                "text": "Welche Vergabeart wird verwendet (öffentliche Ausschreibung, beschränkte Ausschreibung, Verhandlungsverfahren)?",
                "order_index": 2
            },
            {
                "text": "Welche Leistungsbeschreibung wird ausgeschrieben?",
                "order_index": 3
            },
            {
                "text": "Welche Zuschlagskriterien werden angewendet?",
                "order_index": 4
            },
            {
                "text": "Welche Eignungskriterien sind zu erfüllen?",
                "order_index": 5
            },
            {
                "text": "Welche Nachweise sind einzureichen?",
                "order_index": 6
            },
            {
                "text": "Welche Vertragsbedingungen gelten?",
                "order_index": 7
            },
            {
                "text": "Welche Sicherheitsleistungen sind erforderlich?",
                "order_index": 8
            },
            {
                "text": "Welche Zahlungsbedingungen sind vereinbart?",
                "order_index": 9
            },
            {
                "text": "Welche Haftungsregelungen gelten?",
                "order_index": 10
            },
            {
                "text": "Welche Kündigungsmöglichkeiten bestehen?",
                "order_index": 11
            },
            {
                "text": "Welche Nachunternehmerregelungen gelten?",
                "order_index": 12
            },
            {
                "text": "Welche Umwelt- und Nachhaltigkeitskriterien sind zu beachten?",
                "order_index": 13
            },
            {
                "text": "Welche sozialen Kriterien sind zu erfüllen?",
                "order_index": 14
            },
            {
                "text": "Welche technischen Spezifikationen sind vorgegeben?",
                "order_index": 15
            }
        ]
        
        # Create questions
        for q_data in questions:
            question = Question(
                id=str(uuid.uuid4()),
                checklist_id=checklist_id,
                text=q_data["text"],
                order_index=q_data["order_index"],
                created_at=datetime.now()
            )
            db.add(question)
        
        # Conditions for German tender analysis
        conditions = [
            {
                "text": "Das Dokument enthält alle erforderlichen rechtlichen Grundlagen (VgV, SektVO, etc.)",
                "order_index": 1
            },
            {
                "text": "Die Ausschreibung entspricht den Vorgaben der Vergabeverordnung (VgV)",
                "order_index": 2
            },
            {
                "text": "Alle Pflichtangaben nach § 12 VgV sind enthalten",
                "order_index": 3
            },
            {
                "text": "Die Leistungsbeschreibung ist hinreichend bestimmt und verständlich",
                "order_index": 4
            },
            {
                "text": "Die Eignungskriterien sind objektiv und nachprüfbar",
                "order_index": 5
            },
            {
                "text": "Die Zuschlagskriterien sind transparent und gewichtet",
                "order_index": 6
            },
            {
                "text": "Die Fristen entsprechen den gesetzlichen Mindestvorgaben",
                "order_index": 7
            },
            {
                "text": "Die Vergabeart ist sachlich gerechtfertigt",
                "order_index": 8
            },
            {
                "text": "Die Vertragsbedingungen sind angemessen und ausgewogen",
                "order_index": 9
            },
            {
                "text": "Die Sicherheitsleistungen sind verhältnismäßig",
                "order_index": 10
            },
            {
                "text": "Die Zahlungsbedingungen sind marktüblich",
                "order_index": 11
            },
            {
                "text": "Die Haftungsregelungen sind angemessen",
                "order_index": 12
            },
            {
                "text": "Die Nachunternehmerregelungen sind transparent",
                "order_index": 13
            },
            {
                "text": "Umwelt- und Nachhaltigkeitskriterien sind sachlich begründet",
                "order_index": 14
            },
            {
                "text": "Soziale Kriterien sind rechtmäßig und sachlich begründet",
                "order_index": 15
            },
            {
                "text": "Die technischen Spezifikationen sind objektiv und nachprüfbar",
                "order_index": 16
            },
            {
                "text": "Das Dokument enthält keine diskriminierenden Bestimmungen",
                "order_index": 17
            },
            {
                "text": "Die Vergabestelle ist zur Durchführung des Verfahrens berechtigt",
                "order_index": 18
            },
            {
                "text": "Das Verfahren entspricht den Grundsätzen der Transparenz und Gleichbehandlung",
                "order_index": 19
            },
            {
                "text": "Alle erforderlichen Anlagen und Formulare sind beigefügt",
                "order_index": 20
            }
        ]
        
        # Create conditions
        for c_data in conditions:
            condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=checklist_id,
                text=c_data["text"],
                order_index=c_data["order_index"],
                created_at=datetime.now()
            )
            db.add(condition)
        
        # Commit all changes
        db.commit()
        
        print(f"✅ Successfully created German tender checklist with ID: {checklist_id}")
        print(f"📝 Created {len(questions)} questions")
        print(f"🔍 Created {len(conditions)} conditions")
        print(f"📋 Checklist name: {checklist.name}")
        
        return checklist_id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating German checklist: {str(e)}")
        raise
    finally:
        db.close()

def create_additional_templates():
    """Create additional specialized templates."""
    
    db = next(get_db())
    
    try:
        # Template 1: Construction/Construction Services
        construction_id = str(uuid.uuid4())
        construction_checklist = Checklist(
            id=construction_id,
            name="Bauleistungen - Spezialisierte Checkliste",
            description="Spezialisierte Checkliste für Bauleistungen und baunahe Dienstleistungen nach VOB/A und VOF.",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(construction_checklist)
        
        # Construction-specific questions
        construction_questions = [
            {
                "text": "Welche Bauleistungen werden ausgeschrieben?",
                "order_index": 1
            },
            {
                "text": "Welche VOB/A-Bedingungen gelten?",
                "order_index": 2
            },
            {
                "text": "Welche technischen Zeichnungen und Pläne sind erforderlich?",
                "order_index": 3
            },
            {
                "text": "Welche Baustelleneinrichtung ist vorgesehen?",
                "order_index": 4
            },
            {
                "text": "Welche Sicherheitsvorschriften sind zu beachten?",
                "order_index": 5
            }
        ]
        
        for q_data in construction_questions:
            question = Question(
                id=str(uuid.uuid4()),
                checklist_id=construction_id,
                text=q_data["text"],
                order_index=q_data["order_index"],
                created_at=datetime.now()
            )
            db.add(question)
        
        # Construction-specific conditions
        construction_conditions = [
            {
                "text": "Die Ausschreibung entspricht den VOB/A-Bestimmungen",
                "order_index": 1
            },
            {
                "text": "Alle erforderlichen technischen Unterlagen sind vollständig",
                "order_index": 2
            },
            {
                "text": "Die Baustelleneinrichtung ist angemessen berücksichtigt",
                "order_index": 3
            },
            {
                "text": "Die Sicherheitsvorschriften sind vollständig dokumentiert",
                "order_index": 4
            }
        ]
        
        for c_data in construction_conditions:
            condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=construction_id,
                text=c_data["text"],
                order_index=c_data["order_index"],
                created_at=datetime.now()
            )
            db.add(condition)
        
        # Template 2: IT Services
        it_id = str(uuid.uuid4())
        it_checklist = Checklist(
            id=it_id,
            name="IT-Dienstleistungen - Spezialisierte Checkliste",
            description="Spezialisierte Checkliste für IT-Dienstleistungen und Softwareentwicklung.",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(it_checklist)
        
        # IT-specific questions
        it_questions = [
            {
                "text": "Welche IT-Systeme und -Dienstleistungen werden ausgeschrieben?",
                "order_index": 1
            },
            {
                "text": "Welche technischen Anforderungen bestehen?",
                "order_index": 2
            },
            {
                "text": "Welche Sicherheitsstandards sind zu erfüllen?",
                "order_index": 3
            },
            {
                "text": "Welche Wartungs- und Supportleistungen sind erforderlich?",
                "order_index": 4
            }
        ]
        
        for q_data in it_questions:
            question = Question(
                id=str(uuid.uuid4()),
                checklist_id=it_id,
                text=q_data["text"],
                order_index=q_data["order_index"],
                created_at=datetime.now()
            )
            db.add(question)
        
        # IT-specific conditions
        it_conditions = [
            {
                "text": "Die IT-Sicherheitsanforderungen sind vollständig spezifiziert",
                "order_index": 1
            },
            {
                "text": "Die technischen Anforderungen sind objektiv und nachprüfbar",
                "order_index": 2
            },
            {
                "text": "Die Wartungs- und Supportleistungen sind angemessen definiert",
                "order_index": 3
            }
        ]
        
        for c_data in it_conditions:
            condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=it_id,
                text=c_data["text"],
                order_index=c_data["order_index"],
                created_at=datetime.now()
            )
            db.add(condition)
        
        db.commit()
        
        print(f"✅ Successfully created additional templates:")
        print(f"🏗️  Construction checklist: {construction_id}")
        print(f"💻 IT services checklist: {it_id}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating additional templates: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding database with German tender checklists...")
    
    # Create main German checklist
    main_id = create_german_tender_checklist()
    
    # Create additional specialized templates
    create_additional_templates()
    
    print("🎉 Database seeding completed successfully!")
    print(f"📋 Main checklist ID: {main_id}")
    print("🚀 The application now has comprehensive German tender analysis templates!")
