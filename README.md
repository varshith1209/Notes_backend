# NotesAI – AI-Powered Notes Backend

A robust, AI-enhanced backend for a modern note-taking application, featuring semantic search, auto-summarization, and version control.

## Problem Statement
Standard note-taking apps often become cluttered, making it difficult to retrieve information using simple keyword matching. NotesAI solves this by integrating **semantic search** to find notes by meaning and **AI summarization** to quickly digest content, transforming a static repository into an intelligent knowledge base.

## High-Level Overview
The system provides a RESTful API built with **Django** and **Django Rest Framework (DRF)**. It handles user authentication, note management (CRUD), and organization (folders, tags). Background tasks managed by **Celery** and **Redis** handle resource-intensive AI operations like generating vector embeddings and summarizing text, ensuring a responsive user experience.

## Core Features
- **Authentication**: Secure user registration and login using JWT (JSON Web Tokens).
- **Notes Management**: Create, read, update, and delete notes with soft-delete and restore capabilities.
- **Organization**: Structure notes into **Folders** and categorize them with **Tags**.
- **Versioning**: Automatically tracks changes to notes, preserving history in `NoteVersion`.
- **Soft Delete**: Notes are marked as deleted instead of being permanently removed, allowing for restoration.

## Search Capabilities
- **Semantic Search**: Finds notes based on conceptual similarity using vector embeddings.
- **Keyword Search**: Supports traditional text matching (via database filtering).

## AI Functionality
- **Note Summarization**: Asynchronously generates concise summaries of notes using OpenAI (GPT models).
- **Embedding Generation**: Converts note content into vector embeddings using **SentenceTransformers** (Local), **Gemini**, or **OpenAI**.
- **Background Processing**: Utilizes **Celery** with **Redis** to handle AI tasks off the main request/response cycle.

## System Architecture

```ascii
+-------------+       +-------------+       +-------------------------+
|   Client    | <---> |  Django API | <---> | PostgreSQL / SQLite (DB)|
+-------------+       +-------------+       +-------------------------+
                             |
                             v
                      +-------------+
                      |    Redis    |
                      +-------------+
                             |
                             v
                      +-------------+       +-------------------------+
                      |Celery Worker| <---> | AI Models (OpenAI/Local)|
                      +-------------+       +-------------------------+
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Framework** | Django 5.2, Django Rest Framework |
| **Database** | PostgreSQL (Production), SQLite (Dev) |
| **Async Tasks** | Celery, Redis |
| **AI Providers** | OpenAI, Google Gemini, SentenceTransformers |
| **Vector Search** | Numpy (Cosine Similarity), JSONField Storage |
| **Authentication** | JWT (SimpleJWT) |

## Database Schema

```text
User
 ├── Profile (1:1)
 ├── Folder (1:N)
 ├── Tag (1:N)
 └── Note (1:N)
      ├── NoteVersion (1:N)
      ├── Embedding (1:1)
      └── NoteTag (N:M via Tag)
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT pair
- `POST /api/token/refresh/` - Refresh access token

### Folders
- `GET /api/folders/` - List user folders
- `POST /api/folders/` - Create a new folder
- `DELETE /api/folders/<id>/delete/` - Delete a folder

### Notes
- `GET /api/notes/` - List active notes
- `POST /api/notes/` - Create a note
- `GET /api/notes/<id>/` - Retrieve note details
- `PUT /api/notes/<id>/` - Update note (triggers versioning & embedding update)
- `DELETE /api/notes/<id>/` - Soft delete a note
- `POST /api/notes/<id>/favorite/` - Toggle favorite status
- `POST /api/notes/<id>/restore/` - Restore a soft-deleted note

### AI & Search
- `GET /api/search/?q=<query>` - Semantic search for notes
- `POST /api/notes/<id>/summarize/` - Trigger background summarization task

### Tags
- `GET /api/tags/` - List tags
- `POST /api/tags/` - Create a tag
- `GET /api/note-tag/` - List tags associated with notes
- `POST /api/note-tag/` - Attach a tag to a note

## Folder Structure

```text
NotesAI/
├── NotesAI/                # Project settings & configuration
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
├── notes/                  # Core application logic
│   ├── models.py           # Database models (Note, Folder, Embedding)
│   ├── views.py            # API views & business logic
│   ├── tasks.py            # Celery tasks (Summarization)
│   ├── embedding_service.py # Vector generation logic
│   └── summarizer_service.py # AI summarization logic
├── users/                  # User management app
│   ├── models.py           # Profile model
│   └── views.py            # Auth views
├── manage.py               # Django management script
└── .env                    # Environment variables
```

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NotesAI
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   CELERY_BROKER_URL=redis://127.0.0.1:6379/0
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start Redis** (Ensure Redis is installed and running)
   ```bash
   redis-server
   ```

7. **Start Celery Worker**
   ```bash
   celery -A NotesAI worker --loglevel=info
   ```

8. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

## Roadmap
- [ ] **Frontend Integration**: Build a React/Next.js frontend for the API.
- [ ] **PostgreSQL pgvector**: Migrate from in-memory cosine similarity to native database vector search for scalability.
- [ ] **Voice Notes**: Add support for audio transcription and storage.
- [ ] **Shared Notes**: Implement collaboration features for sharing notes between users.

## Why This Project Matters
This project demonstrates the integration of **modern AI capabilities** into a traditional web application architecture. It showcases proficiency in **backend engineering** (Django, DRF), **asynchronous processing** (Celery), and **Applied AI** (Embeddings, LLMs), bridging the gap between standard CRUD apps and intelligent systems.
