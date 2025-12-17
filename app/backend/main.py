from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.backend.core.database import Base, engine
from app.backend.api import budget_routes, expense_routes, saving_routes, advice_routes, auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budgetis", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router)
app.include_router(budget_routes.router)
app.include_router(expense_routes.router)
app.include_router(saving_routes.router)
app.include_router(advice_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.backend.core.database import Base, engine
from app.backend.api import budget_routes, expense_routes, saving_routes, advice_routes, auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budgetis", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router)
app.include_router(budget_routes.router)
app.include_router(expense_routes.router)
app.include_router(saving_routes.router)
app.include_router(advice_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}


