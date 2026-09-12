from fastapi import FastAPI

# This is a minimal deployment entrypoint for Vercel/Azure.
# It is not the production health-validation workflow we removed earlier.
app = FastAPI(title="Commit Analysis Agent")


@app.get("/")
async def root():
    return {
        "service": "Commit Analysis Agent",
        "status": "ok",
        "message": "Deployment endpoint is running."
    }


@app.get("/health")
async def health():
    # Simple readiness check for deployment platforms.
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
