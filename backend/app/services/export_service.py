from typing import List, Dict, Any
import logging
from datetime import datetime
import io

from app.models.document import ProcessedDocument
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

class ExportService:
    """Service for exporting document data"""
    
    def __init__(self):
        self.document_service = DocumentService()
    
    async def prepare_export_data(self, 
                                documents: List[ProcessedDocument], 
                                include_citations: bool = True,
                                include_conflicts: bool = True) -> Dict[str, Any]:
        """Prepare data for export in various formats"""
        
        export_data = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "total_documents": len(documents),
            "documents": []
        }
        
        try:
            for doc in documents:
                # Get document chunks
                chunks = await self.document_service.get_document_chunks(doc.id)
                
                doc_data = {
                    "id": doc.id,
                    "metadata": doc.metadata.dict() if doc.metadata else {},
                    "status": doc.status.value,
                    "total_chunks": len(chunks),
                    "chunks": []
                }
                
                # Add chunk data
                for chunk in chunks:
                    chunk_data = {
                        "chunk_id": chunk.chunk_id,
                        "page": chunk.page_number,
                        "text": chunk.text,
                        "confidence_score": chunk.confidence_score,
                        "metadata": chunk.metadata
                    }
                    doc_data["chunks"].append(chunk_data)
                
                export_data["documents"].append(doc_data)
            
            # Add summary statistics
            total_pages = sum(doc.metadata.total_pages for doc in documents if doc.metadata)
            total_chunks = sum(len(doc_data["chunks"]) for doc_data in export_data["documents"])
            
            export_data["summary"] = {
                "total_pages": total_pages,
                "total_chunks": total_chunks,
                "document_types": list(set(doc.metadata.document_type.value for doc in documents if doc.metadata))
            }
            
        except Exception as e:
            logger.error(f"Failed to prepare export data: {str(e)}")
            raise
        
        return export_data
    
    async def generate_pdf_report(self, export_data: Dict[str, Any]) -> bytes:
        """Generate a PDF report from export data"""
        try:
            # Simple PDF generation - in production, use reportlab or similar
            from io import BytesIO
            
            # This is a placeholder - in a real implementation, you'd use a proper PDF library
            pdf_content = f"""
            SpecScope Document Analysis Report
            Generated: {export_data['export_timestamp']}
            
            Summary:
            - Total Documents: {export_data['total_documents']}
            - Total Pages: {export_data.get('summary', {}).get('total_pages', 'N/A')}
            - Total Chunks: {export_data.get('summary', {}).get('total_chunks', 'N/A')}
            
            Documents:
            """
            
            for doc_data in export_data["documents"]:
                metadata = doc_data["metadata"]
                pdf_content += f"""
                
                Document: {metadata.get('original_filename', 'Unknown')}
                Type: {metadata.get('document_type', 'Unknown')}
                Pages: {metadata.get('total_pages', 'Unknown')}
                Upload Date: {metadata.get('upload_time', 'Unknown')}
                
                Key Sections:
                """
                
                # Add first few chunks as examples
                for chunk in doc_data["chunks"][:3]:
                    pdf_content += f"""
                    Page {chunk['page']}: {chunk['text'][:200]}...
                    """
            
            # Convert to bytes (placeholder - use proper PDF generation)
            return pdf_content.encode('utf-8')
            
        except Exception as e:
            logger.error(f"Failed to generate PDF report: {str(e)}")
            raise