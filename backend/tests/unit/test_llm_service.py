"""Unit tests for LLM service validation."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.services.llm_service import LLMService
import uuid

@pytest.fixture
def llm_service():
    """LLM service for testing."""
    return LLMService()

@pytest.fixture
def sample_document_data():
    """Sample document data for testing."""
    return {
        "id": str(uuid.uuid4()),
        "filename": "test_document.pdf",
        "file_path": "/uploads/test_document.pdf"
    }

@pytest.fixture
def sample_questions():
    """Sample questions for testing."""
    return [
        {"id": str(uuid.uuid4()), "text": "Test question 1?"},
        {"id": str(uuid.uuid4()), "text": "Test question 2?"}
    ]

@pytest.fixture
def sample_conditions():
    """Sample conditions for testing."""
    return [
        {"id": str(uuid.uuid4()), "text": "Test condition 1"},
        {"id": str(uuid.uuid4()), "text": "Test condition 2"}
    ]

def test_llm_service_initialization(llm_service):
    """Test LLM service initialization."""
    assert llm_service is not None
    assert hasattr(llm_service, 'anthropic_client')

@patch('src.services.llm_service.anthropic.AsyncAnthropic')
def test_upload_file_to_anthropic_success(mock_anthropic, llm_service, sample_document_data):
    """Test successful file upload to Anthropic."""
    # Mock Anthropic client
    mock_client = Mock()
    mock_anthropic.return_value = mock_client
    
    # Mock file upload response
    mock_response = Mock()
    mock_response.id = "file_123"
    mock_client.files.create.return_value = mock_response
    
    # Upload file
    result = llm_service.upload_file_to_anthropic(sample_document_data["file_path"])
    
    # Verify result
    assert result == "file_123"
    assert mock_client.files.create.called

@patch('src.services.llm_service.anthropic.AsyncAnthropic')
def test_upload_file_to_anthropic_failure(mock_anthropic, llm_service, sample_document_data):
    """Test file upload to Anthropic failure."""
    # Mock Anthropic client to raise exception
    mock_client = Mock()
    mock_anthropic.return_value = mock_client
    mock_client.files.create.side_effect = Exception("Upload failed")
    
    # Upload file
    with pytest.raises(Exception):
        llm_service.upload_file_to_anthropic(sample_document_data["file_path"])

@patch('src.services.llm_service.anthropic.AsyncAnthropic')
def test_process_document_with_checklist_success(mock_anthropic, llm_service, sample_document_data, sample_questions, sample_conditions):
    """Test successful document processing with checklist."""
    # Mock Anthropic client
    mock_client = Mock()
    mock_anthropic.return_value = mock_client
    
    # Mock message response
    mock_response = Mock()
    mock_response.content = [Mock(text='{"answers": [{"question_id": "q1", "answer": "Test answer 1"}], "conditions": [{"condition_id": "c1", "result": true}]}')]
    mock_client.messages.create.return_value = mock_response
    
    # Process document
    result = llm_service.process_document_with_checklist(
        sample_document_data,
        sample_questions,
        sample_conditions
    )
    
    # Verify result structure
    assert result is not None
    assert "answers" in result
    assert "conditions" in result
    assert len(result["answers"]) == 1
    assert len(result["conditions"]) == 1

@patch('src.services.llm_service.anthropic.AsyncAnthropic')
def test_process_document_with_checklist_failure(mock_anthropic, llm_service, sample_document_data, sample_questions, sample_conditions):
    """Test document processing failure."""
    # Mock Anthropic client to raise exception
    mock_client = Mock()
    mock_anthropic.return_value = mock_client
    mock_client.messages.create.side_effect = Exception("Processing failed")
    
    # Process document
    with pytest.raises(Exception):
        llm_service.process_document_with_checklist(
            sample_document_data,
            sample_questions,
            sample_conditions
        )

def test_validate_api_key_success(llm_service):
    """Test successful API key validation."""
    # Test with valid API key format
    valid_key = "sk-ant-api03-valid-key"
    result = llm_service.validate_api_key(valid_key)
    assert result is True

def test_validate_api_key_failure(llm_service):
    """Test API key validation failure."""
    # Test with invalid API key formats
    invalid_keys = ["", "invalid-key", "sk-invalid", None]
    
    for key in invalid_keys:
        result = llm_service.validate_api_key(key)
        assert result is False

def test_build_prompt_success(llm_service, sample_questions, sample_conditions):
    """Test successful prompt building."""
    # Build prompt
    prompt = llm_service.build_prompt(sample_questions, sample_conditions)
    
    # Verify prompt structure
    assert prompt is not None
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    
    # Verify questions are included
    for question in sample_questions:
        assert question["text"] in prompt
    
    # Verify conditions are included
    for condition in sample_conditions:
        assert condition["text"] in prompt

def test_parse_llm_response_success(llm_service):
    """Test successful LLM response parsing."""
    # Mock LLM response
    mock_response = Mock()
    mock_response.content = [Mock(text='{"answers": [{"question_id": "q1", "answer": "Test answer"}], "conditions": [{"condition_id": "c1", "result": true}]}')]
    
    # Parse response
    result = llm_service.parse_llm_response(mock_response)
    
    # Verify result structure
    assert result is not None
    assert "answers" in result
    assert "conditions" in result

def test_parse_llm_response_invalid_json(llm_service):
    """Test LLM response parsing with invalid JSON."""
    # Mock LLM response with invalid JSON
    mock_response = Mock()
    mock_response.content = [Mock(text='Invalid JSON response')]
    
    # Parse response
    with pytest.raises(Exception):
        llm_service.parse_llm_response(mock_response)

def test_llm_service_with_german_examples(llm_service, sample_document_data):
    """Test LLM service with German tender examples."""
    german_questions = [
        {"id": str(uuid.uuid4()), "text": "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?"},
        {"id": str(uuid.uuid4()), "text": "Wann ist die Frist für die Einreichung von Bieterfragen?"}
    ]
    
    german_conditions = [
        {"id": str(uuid.uuid4()), "text": "Ist die Abgabefrist vor dem 31.12.2025?"}
    ]
    
    # Build prompt with German examples
    prompt = llm_service.build_prompt(german_questions, german_conditions)
    
    # Verify German text is included
    assert "Angebote" in prompt
    assert "Teilnahmeanträge" in prompt
    assert "Bieterfragen" in prompt
    assert "Abgabefrist" in prompt

def test_llm_service_error_handling(llm_service):
    """Test LLM service error handling."""
    # Test with invalid input
    with pytest.raises(Exception):
        llm_service.build_prompt(None, None)
    
    with pytest.raises(Exception):
        llm_service.build_prompt([], [])

def test_llm_service_confidence_scoring(llm_service):
    """Test LLM service confidence scoring."""
    # Mock LLM response with confidence scores
    mock_response = Mock()
    mock_response.content = [Mock(text='{"answers": [{"question_id": "q1", "answer": "Test answer", "confidence": 0.95}], "conditions": [{"condition_id": "c1", "result": true, "confidence": 0.88}]}')]
    
    # Parse response
    result = llm_service.parse_llm_response(mock_response)
    
    # Verify confidence scores are included
    assert "answers" in result
    assert "conditions" in result
    
    # Check if confidence scores are preserved
    if result["answers"] and len(result["answers"]) > 0:
        assert "confidence" in result["answers"][0]
    
    if result["conditions"] and len(result["conditions"]) > 0:
        assert "confidence" in result["conditions"][0]
