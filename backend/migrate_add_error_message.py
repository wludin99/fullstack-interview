#!/usr/bin/env python3
"""Migration script to add error_message field to processing_results table."""

import sqlite3
import os

def migrate():
    """Add error_message column to processing_results table."""
    db_path = "tender_checklist.db"
    
    if not os.path.exists(db_path):
        print("Database not found, skipping migration")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(processing_results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'error_message' not in columns:
            print("Adding error_message column to processing_results table...")
            cursor.execute("ALTER TABLE processing_results ADD COLUMN error_message TEXT")
            conn.commit()
            print("Migration completed successfully")
        else:
            print("error_message column already exists")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
