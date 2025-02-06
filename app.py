from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from Router import delivery, customer, category, food, adminAuth, seting, rider

app = FastAPI()

# register routers
app.include_router(delivery.route)
app.include_router(customer.router)
app.include_router(category.route)
app.include_router(food.route)
app.include_router(adminAuth.route)
app.include_router(seting.route)
app.include_router(rider.route)


# CORS midleware
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost",
    "https://localhost",
    "http://localhost",
    "https://admin.gamage.me",
    "curryhut-admin.netlify.app",
    "https://curryhut-admin.netlify.app",
    "https://curryhut.gamage.me",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
