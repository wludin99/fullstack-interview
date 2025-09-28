"""Anthropic LLM service for document processing."""

import os
from typing import List, Dict, Any
import anthropic
from src.config import settings


class LLMService:
    """Service for Anthropic Claude LLM operations."""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.anthropic_model
    
    def process_document_with_checklist(
        self, 
        document_path: str, 
        questions: List[Dict[str, Any]], 
        conditions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Process a document with a checklist using Claude."""
        
        # Read document content (for now, we'll use a placeholder)
        # In a real implementation, you'd use PDF parsing libraries
        document_content = self._extract_text_from_pdf(document_path)
        
        # Build prompt for Claude
        prompt = self._build_processing_prompt(document_content, questions, conditions)
        
        try:
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.1,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse Claude's response
            return self._parse_llm_response(response.content[0].text, questions, conditions)
            
        except Exception as e:
            return {
                "error": f"LLM processing failed: {str(e)}",
                "answers": [],
                "condition_results": []
            }
    
    def _extract_text_from_pdf(self, document_path: str) -> str:
        """Extract text from PDF document."""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(document_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text if text.strip() else f"Document content from {document_path} - No text extracted from PDF."
        except Exception as e:
            return f"Error extracting text from PDF: {str(e)}"
    
    def _build_processing_prompt(
        self, 
        document_content: str, 
        questions: List[Dict[str, Any]], 
        conditions: List[Dict[str, Any]]
    ) -> str:
        """Build the prompt for Claude to process the document."""
        
        questions_text = "\n".join([
            f"{i+1}. {q['text']}" for i, q in enumerate(questions)
        ])
        
        conditions_text = "\n".join([
            f"{i+1}. {c['text']}" for i, c in enumerate(conditions)
        ])
        
        prompt = f"""You are an expert at analyzing German public tender documents. Please analyze the following document and answer the questions and evaluate the conditions.

DOCUMENT CONTENT:
{document_content}

QUESTIONS TO ANSWER:
{questions_text}

CONDITIONS TO EVALUATE:
{conditions_text}

Please provide your analysis in the following JSON format:
{{
    "answers": [
        {{"questionId": "q1", "answer": "Your answer here"}},
        {{"questionId": "q2", "answer": "Your answer here"}}
    ],
    "condition_results": [
        {{"conditionId": "c1", "result": true}},
        {{"conditionId": "c2", "result": false}}
    ]
}}

Important:
- Answer in German when appropriate for German tender documents
- Be specific and reference the document content
- For conditions, evaluate as true/false based on the document
- If information is not found, state "Information not found in document"
"""
        
        return prompt
    
    def _parse_llm_response(
        self, 
        response_text: str, 
        questions: List[Dict[str, Any]], 
        conditions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Parse Claude's response into structured data."""
        try:
            # This is a simplified parser
            # In production, you'd have more robust JSON parsing
            import json
            
            # Try to extract JSON from the response
            if "{" in response_text and "}" in response_text:
                json_start = response_text.find("{")
                json_end = response_text.rfind("}") + 1
                json_str = response_text[json_start:json_end]
                
                result = json.loads(json_str)
                return result
            else:
                # Fallback: create structured response from text
                return self._create_fallback_response(response_text, questions, conditions)
                
        except Exception as e:
            return {
                "error": f"Failed to parse LLM response: {str(e)}",
                "answers": [],
                "condition_results": []
            }
    
    def _create_fallback_response(
        self, 
        response_text: str, 
        questions: List[Dict[str, Any]], 
        conditions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails."""
        answers = []
        condition_results = []
        
        # Simple text-based parsing as fallback
        for i, question in enumerate(questions):
            answers.append({
                "questionId": f"q{i+1}",
                "answer": f"Answer for: {question['text']} - {response_text[:100]}..."
            })
        
        for i, condition in enumerate(conditions):
            condition_results.append({
                "conditionId": f"c{i+1}",
                "result": "true" in response_text.lower()  # Simple heuristic
            })
        
        return {
            "answers": answers,
            "condition_results": condition_results
        }
    
    def upload_file_to_anthropic(self, file_path: str) -> str:
        """Upload a file to Anthropic File API."""
        try:
            with open(file_path, "rb") as file:
                response = self.client.files.create(
                    file=file,
                    purpose="file-extract"
                )
            return response.id
        except Exception as e:
            raise Exception(f"Failed to upload file to Anthropic: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test connection to Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{
                    "role": "user",
                    "content": "Hello"
                }]
            )
            return True
        except Exception:
            return False
