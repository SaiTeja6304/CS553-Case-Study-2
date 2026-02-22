from fastapi import FastAPI 
from .api_routes import router 
 
# Create FastAPI app
app = FastAPI( 
   title="VLM Chat", 
   version="1.0.0" 
) 
 
 
# Include the routers 
app.include_router(router) 
 