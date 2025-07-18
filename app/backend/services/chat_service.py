import json
from datetime import datetime
from typing import List
from fastapi import HTTPException, status

from backend.db.session import get_db_connection
from backend.services.rag_service import rag_service
from backend.exceptions.custom_exceptions import RAGServiceError
from backend.schemas.chat import ChatHistoryItem

class ChatService:
    @staticmethod
    def process_message(message: str, document_ids: List[str], session_id: str, username: str) -> str:
        """Process chat message using RAG service"""
        if not rag_service.is_ready:
            raise RAGServiceError("Sistem RAG tidak siap. Mohon coba lagi sesaat.")

        try:
            final_response = rag_service.invoke_chain(message, document_ids)
        except Exception as e:
            print(f"Error during RAG chain invocation: {e}")
            final_response = "Maaf, terjadi kesalahan saat memproses permintaan Anda. Silakan coba lagi."

        # Save to database
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO chat_history 
                (session_id, username, message, response, timestamp, document_ids) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            doc_ids_json = json.dumps(document_ids)
            values = (session_id, username, message, final_response, datetime.now(), doc_ids_json)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()

        return final_response
    
    @staticmethod
    def get_session_history(session_id: str, username: str) -> List[ChatHistoryItem]:
        """Get chat history for a specific session"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT message, response, timestamp 
                FROM chat_history 
                WHERE session_id = %s AND username = %s 
                ORDER BY timestamp ASC
            """
            cursor.execute(query, (session_id, username))
            history = cursor.fetchall()
            cursor.close()
        
        formatted_history = []
        for row in history:
            formatted_history.append(ChatHistoryItem(
                sender="user", 
                content=row["message"], 
                timestamp=row["timestamp"]
            ))
            formatted_history.append(ChatHistoryItem(
                sender="assistant", 
                content=row["response"], 
                timestamp=row["timestamp"]
            ))
        
        return formatted_history
    
    @staticmethod
    def delete_session(session_id: str, username: str) -> None:
        """Delete all chat history for a specific session"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            query = """
                DELETE FROM chat_history 
                WHERE session_id = %s AND username = %s
            """
            cursor.execute(query, (session_id, username))
            conn.commit()
            cursor.close()