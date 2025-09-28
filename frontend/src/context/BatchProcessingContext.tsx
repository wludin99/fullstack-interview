import React, { createContext, useContext, useReducer } from 'react';
import type { ReactNode } from 'react';
import type { Document, Checklist, BatchProcessingResponse, BatchProcessingResult } from '../services/api';

// State interface
interface BatchProcessingState {
  // Document management
  documents: Document[];
  selectedDocuments: string[];
  
  // Checklist management
  checklists: Checklist[];
  selectedChecklistId: string | null;
  
  // Processing state
  isProcessing: boolean;
  processingProgress: number;
  batchResults: BatchProcessingResult[];
  batchResponse: BatchProcessingResponse | null;
  
  // UI state
  showTemplateEditor: boolean;
  editingTemplate: Checklist | null;
  error: string | null;
}

// Action types
type BatchProcessingAction =
  | { type: 'SET_DOCUMENTS'; payload: Document[] }
  | { type: 'ADD_DOCUMENT'; payload: Document }
  | { type: 'REMOVE_DOCUMENT'; payload: string }
  | { type: 'SET_SELECTED_DOCUMENTS'; payload: string[] }
  | { type: 'TOGGLE_DOCUMENT_SELECTION'; payload: string }
  | { type: 'SELECT_ALL_DOCUMENTS' }
  | { type: 'DESELECT_ALL_DOCUMENTS' }
  | { type: 'SET_CHECKLISTS'; payload: Checklist[] }
  | { type: 'SET_SELECTED_CHECKLIST'; payload: string | null }
  | { type: 'START_PROCESSING' }
  | { type: 'UPDATE_PROCESSING_PROGRESS'; payload: number }
  | { type: 'SET_BATCH_RESULTS'; payload: BatchProcessingResult[] }
  | { type: 'SET_BATCH_RESPONSE'; payload: BatchProcessingResponse }
  | { type: 'COMPLETE_PROCESSING' }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SHOW_TEMPLATE_EDITOR'; payload: Checklist }
  | { type: 'HIDE_TEMPLATE_EDITOR' }
  | { type: 'RESET_BATCH_STATE' };

// Initial state
const initialState: BatchProcessingState = {
  documents: [],
  selectedDocuments: [],
  checklists: [],
  selectedChecklistId: null,
  isProcessing: false,
  processingProgress: 0,
  batchResults: [],
  batchResponse: null,
  showTemplateEditor: false,
  editingTemplate: null,
  error: null,
};

// Reducer
function batchProcessingReducer(state: BatchProcessingState, action: BatchProcessingAction): BatchProcessingState {
  switch (action.type) {
    case 'SET_DOCUMENTS':
      return { ...state, documents: action.payload };
    
    case 'ADD_DOCUMENT':
      return { ...state, documents: [...state.documents, action.payload] };
    
    case 'REMOVE_DOCUMENT':
      return {
        ...state,
        documents: state.documents.filter(doc => doc.id !== action.payload),
        selectedDocuments: state.selectedDocuments.filter(id => id !== action.payload),
      };
    
    case 'SET_SELECTED_DOCUMENTS':
      return { ...state, selectedDocuments: action.payload };
    
    case 'TOGGLE_DOCUMENT_SELECTION':
      const isSelected = state.selectedDocuments.includes(action.payload);
      return {
        ...state,
        selectedDocuments: isSelected
          ? state.selectedDocuments.filter(id => id !== action.payload)
          : [...state.selectedDocuments, action.payload],
      };
    
    case 'SELECT_ALL_DOCUMENTS':
      return { ...state, selectedDocuments: state.documents.map(doc => doc.id) };
    
    case 'DESELECT_ALL_DOCUMENTS':
      return { ...state, selectedDocuments: [] };
    
    case 'SET_CHECKLISTS':
      return { ...state, checklists: action.payload };
    
    case 'SET_SELECTED_CHECKLIST':
      return { ...state, selectedChecklistId: action.payload };
    
    case 'START_PROCESSING':
      return {
        ...state,
        isProcessing: true,
        processingProgress: 0,
        error: null,
      };
    
    case 'UPDATE_PROCESSING_PROGRESS':
      return { ...state, processingProgress: action.payload };
    
    case 'SET_BATCH_RESULTS':
      return { ...state, batchResults: action.payload };
    
    case 'SET_BATCH_RESPONSE':
      return { ...state, batchResponse: action.payload };
    
    case 'COMPLETE_PROCESSING':
      return {
        ...state,
        isProcessing: false,
        processingProgress: 100,
      };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload, isProcessing: false };
    
    case 'SHOW_TEMPLATE_EDITOR':
      return {
        ...state,
        showTemplateEditor: true,
        editingTemplate: action.payload,
      };
    
    case 'HIDE_TEMPLATE_EDITOR':
      return {
        ...state,
        showTemplateEditor: false,
        editingTemplate: null,
      };
    
    case 'RESET_BATCH_STATE':
      return {
        ...state,
        selectedDocuments: [],
        selectedChecklistId: null,
        isProcessing: false,
        processingProgress: 0,
        batchResults: [],
        batchResponse: null,
        error: null,
      };
    
    default:
      return state;
  }
}

// Context
const BatchProcessingContext = createContext<{
  state: BatchProcessingState;
  dispatch: React.Dispatch<BatchProcessingAction>;
} | null>(null);

// Provider component
export const BatchProcessingProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(batchProcessingReducer, initialState);

  return (
    <BatchProcessingContext.Provider value={{ state, dispatch }}>
      {children}
    </BatchProcessingContext.Provider>
  );
};

// Hook to use the context
export const useBatchProcessing = () => {
  const context = useContext(BatchProcessingContext);
  if (!context) {
    throw new Error('useBatchProcessing must be used within a BatchProcessingProvider');
  }
  return context;
};

// Custom hooks for common operations
export const useBatchProcessingActions = () => {
  const { dispatch } = useBatchProcessing();

  return {
    // Document actions
    setDocuments: (documents: Document[]) => 
      dispatch({ type: 'SET_DOCUMENTS', payload: documents }),
    
    addDocument: (document: Document) => 
      dispatch({ type: 'ADD_DOCUMENT', payload: document }),
    
    removeDocument: (documentId: string) => 
      dispatch({ type: 'REMOVE_DOCUMENT', payload: documentId }),
    
    // Selection actions
    toggleDocumentSelection: (documentId: string) => 
      dispatch({ type: 'TOGGLE_DOCUMENT_SELECTION', payload: documentId }),
    
    selectAllDocuments: () => 
      dispatch({ type: 'SELECT_ALL_DOCUMENTS' }),
    
    deselectAllDocuments: () => 
      dispatch({ type: 'DESELECT_ALL_DOCUMENTS' }),
    
    // Checklist actions
    setChecklists: (checklists: Checklist[]) => 
      dispatch({ type: 'SET_CHECKLISTS', payload: checklists }),
    
    setSelectedChecklist: (checklistId: string | null) => 
      dispatch({ type: 'SET_SELECTED_CHECKLIST', payload: checklistId }),
    
    // Processing actions
    startProcessing: () => 
      dispatch({ type: 'START_PROCESSING' }),
    
    updateProcessingProgress: (progress: number) => 
      dispatch({ type: 'UPDATE_PROCESSING_PROGRESS', payload: progress }),
    
    setBatchResults: (results: BatchProcessingResult[]) => 
      dispatch({ type: 'SET_BATCH_RESULTS', payload: results }),
    
    setBatchResponse: (response: BatchProcessingResponse) => 
      dispatch({ type: 'SET_BATCH_RESPONSE', payload: response }),
    
    completeProcessing: () => 
      dispatch({ type: 'COMPLETE_PROCESSING' }),
    
    setError: (error: string | null) => 
      dispatch({ type: 'SET_ERROR', payload: error }),
    
    // Template editor actions
    showTemplateEditor: (template: Checklist) => 
      dispatch({ type: 'SHOW_TEMPLATE_EDITOR', payload: template }),
    
    hideTemplateEditor: () => 
      dispatch({ type: 'HIDE_TEMPLATE_EDITOR' }),
    
    // Reset action
    resetBatchState: () => 
      dispatch({ type: 'RESET_BATCH_STATE' }),
  };
};

// Selector hooks for computed values
export const useBatchProcessingSelectors = () => {
  const { state } = useBatchProcessing();

  return {
    // Document selectors
    selectedDocuments: state.documents.filter(doc => 
      state.selectedDocuments.includes(doc.id)
    ),
    
    unselectedDocuments: state.documents.filter(doc => 
      !state.selectedDocuments.includes(doc.id)
    ),
    
    // Checklist selectors
    selectedChecklist: state.checklists.find(checklist => 
      checklist.id === state.selectedChecklistId
    ),
    
    templates: state.checklists.filter(checklist => 
      checklist.name.includes('Template') || checklist.name.includes('Standard')
    ),
    
    customChecklists: state.checklists.filter(checklist => 
      !checklist.name.includes('Template') && !checklist.name.includes('Standard')
    ),
    
    // Processing selectors
    canStartProcessing: state.selectedChecklistId !== null && 
                       state.selectedDocuments.length > 0 && 
                       !state.isProcessing,
    
    processingStatus: state.isProcessing ? 'processing' : 
                     state.batchResults.length > 0 ? 'completed' : 'idle',
    
    successCount: state.batchResults.filter(result => result.status === 'completed').length,
    
    errorCount: state.batchResults.filter(result => result.status === 'error').length,
    
    // UI selectors
    showResults: state.batchResults.length > 0,
    
    hasError: state.error !== null,
  };
};
