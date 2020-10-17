from fastapi import FastAPI

from youtube_podcast_api.routers import user


# Create the FastAPI app
app = FastAPI()

# Add routes
app.include_router(user.router)
