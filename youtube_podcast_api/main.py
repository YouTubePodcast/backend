from fastapi import FastAPI

from youtube_podcast_api.routers import user, auth


# Create the FastAPI app
app = FastAPI()

# Add routes
app.include_router(user.router)
app.include_router(auth.router)
