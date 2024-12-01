# Django Scraping and API Project

## Project Overview

This is a Django-based application for scraping and managing data across the following categories:
- **Vikings NFL**
- **Vikings**
- **Norsemen**

The project includes:
- An admin dashboard for managing users and data.
- APIs with filtering, searching, and ordering capabilities using Django Filters.

---

## Installation and Setup

### Prerequisites
- Docker
- Docker Compose

### Steps to Run the Project

1. **Clone the Repository**
   ```bash
   git clone git@github.com:diellor/data-eng.git
   cd data-eng
   ```

2. **Build and Start the Application**
   ```bash
   docker compose up -d --build
   ```
   This will:
   - Seed the database with initial data.
   - Create a default admin user.
   - Populate scraper-related data.

3. **Access the Application**
   - **Admin Dashboard**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
     - **Username**: `test`
     - **Password**: `testtest`
     - **Email**: `test@example.com`
   - **APIs**: [http://localhost:8000/api/](http://localhost:8000/api/)

---

## API Endpoints and Features

### 1. Vikings NFL API
- **Endpoint**: `/api/vikings_nfl/`
- **Search Fields**: `player_name`, `profile_link`, `age`
- **Filter Fields**: `player_name`, `profile_link`
- **Ordering Fields**: `actor_name`, `character_name`

#### Example Usage
- **Retrieve all records**:
  ```
  http://localhost:8000/api/vikings_nfl/
  ```
- **Search for a player by name**:
  ```
  http://localhost:8000/api/vikings_nfl?player_name=Cam Akers
  ```
- **Filter by profile link**:
  ```
 http://localhost:8000/api/vikings_nfl/?profile_link=https://www.vikings.com/team/players-roster/jordan-addison/  ```
- **Order by player name**:
  ```
  http://localhost:8000/api/vikings_nfl?ordering=Cam Akers
  ```

### 2. Vikings API
- **Endpoint**: `/api/vikings/`
- **Search Fields**: `actor_url`, `img_src`, `actor_name`, `character_name`, `character_description`
- **Filter Fields**: `actor_url`, `actor_name`, `character_name`
- **Ordering Fields**: `actor_name`, `character_name`

#### Example Usage
- **Retrieve all records**:
  ```
  http://localhost:8000/api/vikings/
  ```
- **Search for an actor by name**:
  ```
  http://localhost:8000/api/vikings?actor_name=<REPLACE_WITH_EXISTING_NAME>
  ```
- **Filter by character name**:
  ```
  http://localhost:8000/api/vikings?character_name=<REPLACE_WITH_EXISTING_NAME>
  ```
- **Order by actor name**:
  ```
  http://localhost:8000/api/vikings?ordering=<REPLACE_WITH_EXISTING_NAME>
  ```

### 3. Norsemen API
- **Endpoint**: `/api/norsemen/`
- **Search Fields**: `actor_name`, `character_name`, `description`
- **Filter Fields**: `actor_name`, `character_name`
- **Ordering Fields**: `actor_name`, `character_name`

#### Example Usage
- **Retrieve all records**:
  ```
  http://localhost:8000/api/norsemen/
  ```
- **Search for a character by name**:
  ```
  http://localhost:8000/api/norsemen?character_name=Marian Saastad Ottesen
  ```
- **Filter by actor name**:
  ```
  http://localhost:8000/api/norsemen?actor_name=Hildur
  ```
- **Order by character name**:
  ```
  http://localhost:8000/api/norsemen?ordering=Marian Saastad Ottesen
  ```

---

## Technical Details

- **Backend**: Django
- **Database**: PostgreSQL (via Docker)
- **API Framework**: Django REST Framework (DRF) with Django Filters
- **Containerization**: Docker and Docker Compose

---

## Configuration

To modify configurations:
1. Edit the `.env` file as needed.
2. Rebuild the Docker containers:
   ```bash
   docker compose up -d --build
   ```

## Troubleshooting

1. Ensure Docker and Docker Compose are installed and running correctly.
2. Verify that ports (e.g., `8000`) are not already in use.
3. Restart the application:
   ```bash
   docker compose down
   docker compose up -d
   ```

---

