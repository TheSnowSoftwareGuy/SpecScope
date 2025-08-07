export type SearchResult = {
  chunk_id: string;
  document_id: string;
  filename: string;
  page_number: number;
  section?: string;
  snippet: string;
  highlights: string[];
  scores: { vector: number; keyword: number; hybrid: number };
  confidence: number;
};

export type Citation = {
  chunk_id: string;
  document_id: string;
  filename: string;
  page_number: number;
  section?: string;
  quote: string;
  char_start: number;
  char_end: number;
};

export type QAResponse = {
  answer: string;
  citations: Citation[];
  confidence: number;
  used_chunks: any[];
};