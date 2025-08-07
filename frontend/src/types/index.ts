export interface DocumentMetadata {
  filename: string;
  original_filename: string;
  file_size: number;
  upload_time: string;
  total_pages: number;
  document_type: 'specification' | 'addendum' | 'rfp' | 'drawings' | 'other';
  project_name?: string;
  division?: string;
  section?: string;
}

export interface ProcessedDocument {
  id: string;
  metadata: DocumentMetadata | null;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  processing_time?: number;
  error_message?: string;
  text_chunks?: Array<{
    chunk_id: string;
    text: string;
    page: number;
  }>;
  embedding_ids?: string[];
}

export interface Citation {
  document_id: string;
  document_name: string;
  page_number: number;
  chunk_id: string;
  text_snippet: string;
  confidence_score: number;
  exact_match: boolean;
}

export interface SearchResult {
  query: string;
  search_type: 'keyword' | 'semantic' | 'hybrid';
  total_results: number;
  processing_time: number;
  results: Citation[];
  conflicts: Array<{
    type: string;
    description: string;
    documents: Array<{
      id: string;
      name: string;
      page: number;
      text: string;
    }>;
    severity: string;
  }>;
  suggestions: string[];
}

export interface SearchRequest {
  query: string;
  search_type?: 'keyword' | 'semantic' | 'hybrid';
  document_ids?: string[];
  max_results?: number;
  include_context?: boolean;
  min_confidence?: number;
}

export interface UploadProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  result?: ProcessedDocument;
  error?: string;
}