# SOL-BACKEND-FREE

This repository hosts a FastAPI backend that interacts with the Solana blockchain to manage NFT data. It provides RESTful API endpoints to serve data to the frontend, facilitating the display and interaction with NFTs.

## Features

- **Blockchain Interaction**: Interfaces with the Solana blockchain to fetch and update NFT data.
- **REST API**: Exposes endpoints that serve NFT data to the frontend application.
- **Database Management**: Keeps track of NFTs in a database, ensuring up-to-date information.
- **Testing Support**: A test directory is available for inserting NFT data into the database and testing the reading of Solana NFTs.
- **Configurable Environment**: Environment variables control various aspects of the application, including database connections and API endpoints.

## Getting Started

### Prerequisites

- Python 3.9 or later
- [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL (or any other supported database)

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/arnon3339/sol-backend-free.git
    cd sol-backend-free
    ```

2. **Initialize the submodule**:

    ```bash
    git submodule update --init --recursive
    ```

3. **Install dependencies**:

    Create and activate a virtual environment, then install the required Python packages.

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:

    Set up necessary environment variables in a `.env` file. Below are the environment variables used:

    ```plaintext
    ENV=your_environment
    POSTGRES_PROD=your_production_database_url
    POSTGRES_DEV=your_development_database_url
    ENDPOINT=your_solona_endpoint
    COLLECTIONKEY=your_collection_key
    CANDY_PROGRAM_ID=your_candy_program_id
    CANDY_GUARD_ID=your_candy_guard_id
    CANDY_MINT_ACC=your_candy_mint_account
    MINTSIGNATURE=your_mint_signature
    ```

5. **Run the application**:

    Start the FastAPI application.

    ```bash
    uvicorn main:app --reload
    ```