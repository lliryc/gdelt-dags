from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://airflow:airflow@127.0.0.1/gdelt")

search_service_app = FastAPI()

# Add CORS middleware
search_service_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create an async engine
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

DEFAULT_PROJECTION = [
    "record_uuid", "document_identifier", "themes", "themes_enhanced", 
    "persons", "persons_enhanced", "organizations", "organizations_enhanced", 
    "locations", "locations_enhanced",
    "sharing_image", "all_names", "quotations", "extras_xml", "date_dt"
]

@search_service_app.get("/search/")
async def search(
    query: str,
    top_k: int = Query(default=100, ge=5, le=100, description="Number of results to return"),
    projection: List[str] = Query(default=DEFAULT_PROJECTION, description="List of columns to return")
):
    # Validate projection columns
    valid_columns = set(DEFAULT_PROJECTION)
    invalid_columns = set(projection) - valid_columns
    if invalid_columns:
        raise HTTPException(status_code=400, detail=f"Invalid columns in projection: {', '.join(invalid_columns)}")

    # Create the SELECT part of the query
    select_columns = ", ".join(projection)
    sql_query = f"SELECT {select_columns} FROM raw.gkg_raw gr WHERE tsv_content @@ plainto_tsquery(:query) and trans_type='en' and extras_xml like '%<PAGE_TITLE>%' ORDER BY date_dt DESC LIMIT :top_k"
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(text(sql_query), {'query': query, 'top_k': top_k, 'select_columns': select_columns})
        records = result.fetchall()
        
        if not records:
            raise HTTPException(status_code=404, detail="No records found")
        
        return [dict(record._mapping) for record in records]

if __name__ == "__main__":
    uvicorn.run(search_service_app, host="0.0.0.0", port=8000)