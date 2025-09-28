"""
Data seeding module for the Tender Checklist App.
Automatically populates the database with comprehensive German tender checklists.
"""

import uuid
import shutil
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
from src.models.document import Document

def seed_german_checklists(db: Session):
    """Seed the database with comprehensive German tender checklists."""
    
    # Check if checklists already exist
    existing_checklists = db.query(Checklist).filter(
        Checklist.name.like("%Deutsche Ausschreibung%")
    ).first()
    
    if existing_checklists:
        print("📋 German checklists already exist, skipping seed.")
        return
    
    # Also seed documents if they don't exist
    seed_german_documents(db)
    
    try:
        # Create main comprehensive German checklist
        main_checklist_id = str(uuid.uuid4())
        main_checklist = Checklist(
            id=main_checklist_id,
            name="Deutsche Ausschreibung - Vollständige Checkliste",
            description="Umfassende Checkliste für die Analyse deutscher öffentlicher Ausschreibungen. Deckt alle wichtigen Aspekte von Vergabeverfahren ab.",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(main_checklist)
        
        # Comprehensive questions for German tender analysis
        questions_data = [
            "Was ist der Abgabetermin für die Teilnahmeanträge?",
            "Welche Vergabeart wird verwendet (öffentliche Ausschreibung, beschränkte Ausschreibung, Verhandlungsverfahren)?",
            "Welche Leistungsbeschreibung wird ausgeschrieben?",
            "Welche Zuschlagskriterien werden angewendet?",
            "Welche Eignungskriterien sind zu erfüllen?",
            "Welche Nachweise sind einzureichen?",
            "Welche Vertragsbedingungen gelten?",
            "Welche Sicherheitsleistungen sind erforderlich?",
            "Welche Zahlungsbedingungen sind vereinbart?",
            "Welche Haftungsregelungen gelten?",
            "Welche Kündigungsmöglichkeiten bestehen?",
            "Welche Nachunternehmerregelungen gelten?",
            "Welche Umwelt- und Nachhaltigkeitskriterien sind zu beachten?",
            "Welche sozialen Kriterien sind zu erfüllen?",
            "Welche technischen Spezifikationen sind vorgegeben?"
        ]
        
        for i, question_text in enumerate(questions_data, 1):
            question = Question(
                id=str(uuid.uuid4()),
                checklist_id=main_checklist_id,
                text=question_text,
                order_index=i,
                created_at=datetime.now()
            )
            db.add(question)
        
        # Comprehensive conditions for German tender analysis
        conditions_data = [
            "Das Dokument enthält alle erforderlichen rechtlichen Grundlagen (VgV, SektVO, etc.)",
            "Die Ausschreibung entspricht den Vorgaben der Vergabeverordnung (VgV)",
            "Alle Pflichtangaben nach § 12 VgV sind enthalten",
            "Die Leistungsbeschreibung ist hinreichend bestimmt und verständlich",
            "Die Eignungskriterien sind objektiv und nachprüfbar",
            "Die Zuschlagskriterien sind transparent und gewichtet",
            "Die Fristen entsprechen den gesetzlichen Mindestvorgaben",
            "Die Vergabeart ist sachlich gerechtfertigt",
            "Die Vertragsbedingungen sind angemessen und ausgewogen",
            "Die Sicherheitsleistungen sind verhältnismäßig",
            "Die Zahlungsbedingungen sind marktüblich",
            "Die Haftungsregelungen sind angemessen",
            "Die Nachunternehmerregelungen sind transparent",
            "Umwelt- und Nachhaltigkeitskriterien sind sachlich begründet",
            "Soziale Kriterien sind rechtmäßig und sachlich begründet",
            "Die technischen Spezifikationen sind objektiv und nachprüfbar",
            "Das Dokument enthält keine diskriminierenden Bestimmungen",
            "Die Vergabestelle ist zur Durchführung des Verfahrens berechtigt",
            "Das Verfahren entspricht den Grundsätzen der Transparenz und Gleichbehandlung",
            "Alle erforderlichen Anlagen und Formulare sind beigefügt"
        ]
        
        for i, condition_text in enumerate(conditions_data, 1):
            condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=main_checklist_id,
                text=condition_text,
                order_index=i,
                created_at=datetime.now()
            )
            db.add(condition)
        
        # Create specialized templates
        create_construction_template(db)
        create_it_template(db)
        create_consulting_template(db)
        
        db.commit()
        print("✅ Successfully seeded database with comprehensive German tender checklists")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {str(e)}")
        raise

def create_construction_template(db: Session):
    """Create construction services template."""
    checklist_id = str(uuid.uuid4())
    checklist = Checklist(
        id=checklist_id,
        name="Bauleistungen - Spezialisierte Checkliste",
        description="Spezialisierte Checkliste für Bauleistungen und baunahe Dienstleistungen nach VOB/A und VOF.",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(checklist)
    
    # Construction questions
    construction_questions = [
        "Welche Bauleistungen werden ausgeschrieben?",
        "Welche VOB/A-Bedingungen gelten?",
        "Welche technischen Zeichnungen und Pläne sind erforderlich?",
        "Welche Baustelleneinrichtung ist vorgesehen?",
        "Welche Sicherheitsvorschriften sind zu beachten?",
        "Welche Umweltauflagen sind zu erfüllen?",
        "Welche Gewährleistungsregelungen gelten?"
    ]
    
    for i, question_text in enumerate(construction_questions, 1):
        question = Question(
            id=str(uuid.uuid4()),
            checklist_id=checklist_id,
            text=question_text,
            order_index=i,
            created_at=datetime.now()
        )
        db.add(question)
    
    # Construction conditions
    construction_conditions = [
        "Die Ausschreibung entspricht den VOB/A-Bestimmungen",
        "Alle erforderlichen technischen Unterlagen sind vollständig",
        "Die Baustelleneinrichtung ist angemessen berücksichtigt",
        "Die Sicherheitsvorschriften sind vollständig dokumentiert",
        "Die Umweltauflagen sind vollständig spezifiziert",
        "Die Gewährleistungsregelungen sind angemessen"
    ]
    
    for i, condition_text in enumerate(construction_conditions, 1):
        condition = Condition(
            id=str(uuid.uuid4()),
            checklist_id=checklist_id,
            text=condition_text,
            order_index=i,
            created_at=datetime.now()
        )
        db.add(condition)

def create_it_template(db: Session):
    """Create IT services template."""
    checklist_id = str(uuid.uuid4())
    checklist = Checklist(
        id=checklist_id,
        name="IT-Dienstleistungen - Spezialisierte Checkliste",
        description="Spezialisierte Checkliste für IT-Dienstleistungen und Softwareentwicklung.",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(checklist)
    
    # IT questions
    it_questions = [
        "Welche IT-Systeme und -Dienstleistungen werden ausgeschrieben?",
        "Welche technischen Anforderungen bestehen?",
        "Welche Sicherheitsstandards sind zu erfüllen?",
        "Welche Wartungs- und Supportleistungen sind erforderlich?",
        "Welche Datenverarbeitungsregelungen gelten?",
        "Welche Lizenzbedingungen sind zu beachten?"
    ]
    
    for i, question_text in enumerate(it_questions, 1):
        question = Question(
            id=str(uuid.uuid4()),
            checklist_id=checklist_id,
            text=question_text,
            order_index=i,
            created_at=datetime.now()
        )
        db.add(question)
    
    # IT conditions
    it_conditions = [
        "Die IT-Sicherheitsanforderungen sind vollständig spezifiziert",
        "Die technischen Anforderungen sind objektiv und nachprüfbar",
        "Die Wartungs- und Supportleistungen sind angemessen definiert",
        "Die Datenverarbeitungsregelungen entsprechen der DSGVO",
        "Die Lizenzbedingungen sind transparent und angemessen"
    ]
    
    for i, condition_text in enumerate(it_conditions, 1):
        condition = Condition(
            id=str(uuid.uuid4()),
            checklist_id=checklist_id,
            text=condition_text,
            order_index=i,
            created_at=datetime.now()
        )
        db.add(condition)

def create_consulting_template(db: Session):
    """Create consulting services template."""
    checklist_id = str(uuid.uuid4())
    checklist = Checklist(
        id=checklist_id,
        name="Beratungsleistungen - Spezialisierte Checkliste",
        description="Spezialisierte Checkliste für Beratungsleistungen und Dienstleistungen.",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(checklist)
    
    # Consulting questions
    consulting_questions = [
        "Welche Beratungsleistungen werden ausgeschrieben?",
        "Welche Qualifikationsanforderungen bestehen?",
        "Welche Referenzen sind erforderlich?",
        "Welche Vertraulichkeitsregelungen gelten?",
        "Welche Leistungsnachweise sind zu erbringen?"
    ]
    
    for i, question_text in enumerate(consulting_questions, 1):
        question = Question(
            id=str(uuid.uuid4()),
            checklist_id=checklist_id,
            text=question_text,
            order_index=i,
            created_at=datetime.now()
        )
        db.add(question)
    
    # Consulting conditions
    consulting_conditions = [
        "Die Qualifikationsanforderungen sind objektiv und nachprüfbar",
        "Die Referenzanforderungen sind angemessen",
        "Die Vertraulichkeitsregelungen sind vollständig spezifiziert",
        "Die Leistungsnachweise sind klar definiert"
    ]
    
    for i, condition_text in enumerate(consulting_conditions, 1):
        condition = Condition(
            id=str(uuid.uuid4()),
            checklist_id=checklist_id,
            text=condition_text,
            order_index=i,
            created_at=datetime.now()
        )
        db.add(condition)

def seed_german_documents(db: Session):
    """Seed the database with German tender documents."""
    
    # Check if documents already exist
    existing_docs = db.query(Document).filter(
        Document.original_name.like("%.pdf")
    ).first()
    
    if existing_docs:
        print("📄 German documents already exist, skipping seed.")
        return
    
    # Path to the Tender_documents folder
    tender_docs_path = Path(__file__).parent.parent.parent / "Tender_documents"
    
    if not tender_docs_path.exists():
        print(f"⚠️  Tender_documents folder not found at: {tender_docs_path}")
        return
    
    # List of documents to upload
    documents_to_upload = [
        "Bewerbungsbedingungen.pdf",
        "Fragebogen zur Eignungspruefung.pdf", 
        "KAT5.pdf"
    ]
    
    uploaded_count = 0
    
    try:
        for doc_name in documents_to_upload:
            doc_path = tender_docs_path / doc_name
            
            if not doc_path.exists():
                print(f"⚠️  Document not found: {doc_name}")
                continue
            
            # Create uploads directory if it doesn't exist
            uploads_dir = Path(__file__).parent.parent / "uploads"
            uploads_dir.mkdir(exist_ok=True)
            
            # Generate unique filename
            doc_id = str(uuid.uuid4())
            filename = f"{doc_id}.pdf"
            file_path = uploads_dir / filename
            
            # Copy the document to uploads directory
            shutil.copy2(doc_path, file_path)
            
            # Get file size
            file_size = doc_path.stat().st_size
            
            # Create document record
            document = Document(
                id=doc_id,
                filename=filename,
                original_name=doc_name,
                file_path=str(file_path),
                file_size=file_size,
                status="uploaded",
                uploaded_at=datetime.now()
            )
            
            db.add(document)
            uploaded_count += 1
            
        db.commit()
        print(f"✅ Successfully seeded {uploaded_count} German tender documents")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding documents: {str(e)}")
        raise