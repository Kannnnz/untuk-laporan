import shutil
from pathlib import Path
from typing import List

# LangChain and related imports
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

# Local application imports
from backend.core import config
from backend.db.session import get_db_connection

class RAGService:
    """
    Manages all Retrieval-Augmented Generation (RAG) functionalities.
    """
    def __init__(self):
        self.vector_store: FAISS | None = None
        self.retrieval_chain = None
        # ### PERBAIKAN ###: Simpan document_chain sebagai atribut terpisah
        self.document_chain = None
        self.is_ready = False
        try:
            self._initialize_components()
            self.is_ready = True
            print("✅ RAG components are ready.")
        except Exception as e:
            print(f"❌ CRITICAL ERROR: Failed to initialize RAG components. Error: {e}")

    def _initialize_components(self):
        """Initializes all core components of the RAG system."""
        embeddings = OllamaEmbeddings(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL)
        llm = OllamaLLM(model=config.OLLAMA_MODEL, base_url=config.OLLAMA_BASE_URL)
        
        prompt_template = ChatPromptTemplate.from_template("""
        Anda adalah asisten AI yang berfokus pada lingkungan akademik Universitas Negeri Semarang (UNNES).
        Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan konteks yang diberikan di bawah ini.
        Jika konteks tidak mengandung jawaban, atau jika pertanyaan tidak relevan dengan konteks, Anda HARUS menolak untuk menjawab.
        Contoh penolakan: "Maaf, informasi tersebut tidak ditemukan dalam dokumen yang diberikan."
        JANGAN menjawab pertanyaan umum atau di luar topik konteks yang diberikan. JAWAB SELALU DALAM BAHASA INDONESIA.
        
        INSTRUKSI KHUSUS UNTUK RINGKASAN:
        Jika pertanyaan meminta ringkasan dokumen (seperti "Buat ringkasan dari dokumen ini", "ringkasan", "summarize", dll), 
        berikan jawaban yang PANJANG, DETAIL, dan KOMPREHENSIF dengan:
        1. Pendahuluan singkat tentang dokumen
        2. Poin-poin utama yang dibahas secara detail
        3. Metodologi atau pendekatan yang digunakan (jika ada)
        4. Temuan atau hasil penting
        5. Kesimpulan atau implikasi
        6. Gunakan paragraf yang terstruktur dan informatif
        7. Minimal 200-300 kata untuk ringkasan

        Konteks: {context}
        Pertanyaan: {input}
        Jawaban Informatif:""")
        
        # ### PERBAIKAN ###: Buat dan simpan document_chain ke self.document_chain
        self.document_chain = create_stuff_documents_chain(llm, prompt_template)
        
        if config.FAISS_INDEX_PATH.exists():
            print(f"Loading existing FAISS index from {config.FAISS_INDEX_PATH}...")
            self.vector_store = FAISS.load_local(str(config.VECTOR_STORE_DIR), embeddings, "unnes_docs", allow_dangerous_deserialization=True)
        else:
            print("No FAISS index found. Creating a new one...")
            self.vector_store = FAISS.from_documents([Document(page_content="init")], embeddings)
            self.save_index()
            
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={'k': 5})
        
        # ### PERBAIKAN ###: Gunakan self.document_chain yang sudah disimpan
        self.retrieval_chain = create_retrieval_chain(retriever, self.document_chain)

    def save_index(self):
        if self.vector_store:
            self.vector_store.save_local(str(config.VECTOR_STORE_DIR), "unnes_docs")
    
    def add_documents_to_index(self, chunks: List[Document]):
        if self.vector_store:
            self.vector_store.add_documents(chunks)
            self.save_index()
            self._update_retriever()
            
    def _update_retriever(self):
        if self.vector_store and self.document_chain:
            retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={'k': 5})
            # ### PERBAIKAN ###: Gunakan self.document_chain yang sudah disimpan, bukan dari self.retrieval_chain
            self.retrieval_chain = create_retrieval_chain(retriever, self.document_chain)

    def invoke_chain(self, message: str, doc_ids: List[str] | None = None):
        if not self.is_ready:
            raise Exception("RAG Service is not ready.")
        
        chain_to_invoke = self.retrieval_chain
        if doc_ids:
            doc_filter = {"doc_id": {"$in": doc_ids}}
            filtered_retriever = self.vector_store.as_retriever(search_kwargs={'k': 5, 'filter': doc_filter})
            # ### PERBAIKAN ###: Gunakan self.document_chain yang sudah disimpan
            chain_to_invoke = create_retrieval_chain(filtered_retriever, self.document_chain)
        
        response_data = chain_to_invoke.invoke({"input": message})
        return response_data.get("answer", "Tidak ada jawaban yang ditemukan.")

    def remove_documents_from_index(self, doc_id: str):
        """Remove specific document from vector store by doc_id (faster than full rebuild)"""
        if not self.vector_store:
            return False
            
        try:
            # Get all document IDs in the vector store
            all_docs = self.vector_store.docstore._dict
            docs_to_remove = []
            
            # Find documents with matching doc_id (optimized with list comprehension)
            docs_to_remove = [doc_key for doc_key, doc in all_docs.items() 
                            if doc.metadata.get('doc_id') == doc_id]
            
            # Remove documents from docstore and index
            if docs_to_remove:
                # Batch removal for better performance
                for doc_key in docs_to_remove:
                    del self.vector_store.docstore._dict[doc_key]
                
                # Update index mapping
                remaining_docs = list(self.vector_store.docstore._dict.values())
                if remaining_docs:
                    # Only rebuild if we have remaining documents
                    embeddings = self.vector_store.embeddings
                    new_vector_store = FAISS.from_documents(remaining_docs, embeddings)
                    self.vector_store = new_vector_store
                else:
                    # If no documents left, create minimal empty index
                    embeddings = self.vector_store.embeddings
                    self.vector_store = FAISS.from_documents([Document(page_content="init")], embeddings)
                
                # Save index asynchronously if possible
                self.save_index()
                self._update_retriever()
                print(f"✅ Document {doc_id} removed from index successfully. Removed {len(docs_to_remove)} chunks.")
                return True
            else:
                print(f"⚠️ Document {doc_id} not found in index.")
                return True
                
        except Exception as e:
            print(f"❌ Error removing document from index: {e}")
            # Fallback to full rebuild if removal fails
            print("🔄 Falling back to full index rebuild...")
            return self.rebuild_index()

    def rebuild_index(self):
        print("Rebuilding FAISS index...")
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT file_path, id, filename, username FROM documents WHERE is_indexed = 1")
                all_docs = cursor.fetchall()
                cursor.close()
            
            embeddings = self.vector_store.embeddings
            all_chunks = []

            if not all_docs:
                if config.VECTOR_STORE_DIR.exists(): shutil.rmtree(config.VECTOR_STORE_DIR)
                config.VECTOR_STORE_DIR.mkdir()
                new_vector_store = FAISS.from_documents([Document(page_content="init")], embeddings)
            else:
                for doc in all_docs:
                    file_path = Path(doc["file_path"])
                    if not file_path.is_absolute(): file_path = config.BASE_DIR / file_path
                    
                    if file_path.exists():
                        chunks = load_and_split_document(file_path)
                        for chunk in chunks:
                            chunk.metadata.update({"doc_id": doc["id"], "filename": doc["filename"], "owner": doc["username"]})
                        all_chunks.extend(chunks)
                
                if not all_chunks: all_chunks.append(Document(page_content="init"))
                new_vector_store = FAISS.from_documents(all_chunks, embeddings)

            self.vector_store = new_vector_store
            self.save_index()
            self._update_retriever()
            print("✅ FAISS index rebuilt successfully.")
            return True
        except Exception as e:
            print(f"❌ CRITICAL ERROR during FAISS rebuild: {e}")
            return False

def load_and_split_document(file_path: Path) -> List[Document]:
    ext = file_path.suffix.lower()
    if ext == ".pdf": loader = PyPDFLoader(str(file_path))
    elif ext in [".docx", ".doc"]: loader = Docx2txtLoader(str(file_path))
    elif ext == ".txt": loader = TextLoader(str(file_path), encoding='utf-8')
    else: return []
    
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    return text_splitter.split_documents(documents)

rag_service = RAGService()