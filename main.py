from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import workout_collection, user_collection
from bson import ObjectId

app = FastAPI(title="Workout Buddy API")

# Angular (Frontend) ko connect karne ke liye CORS policy allow karna zaroori hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], # Angular ka default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB data ko JSON format mein theek karne ke liye helper function
def workout_helper(workout) -> dict:
    return {
        "id": str(workout["_id"]),
        "name": workout.get("name"),
        "category": workout.get("category"), # eg. Chest, Cardio
        "duration": workout.get("duration")  # eg. 30 mins
    }

# ================= USER ROUTES =================

@app.post("/api/login")
async def login_user(user_data: dict):
    # Professional app mein hum password check karte hain. 
    user = await user_collection.find_one({"email": user_data.get("email"), "password": user_data.get("password")})
    
    if user:
        # Check karenge ki user 'admin' hai ya normal 'user'
        return {
            "message": "Login successful", 
            "role": user.get("role", "user"), 
            "user_id": str(user["_id"])
        }
    raise HTTPException(status_code=401, detail="Galat Email ya Password")

# ================= WORKOUT ROUTES =================

# Saare workouts fetch karne ke liye (User aur Admin dono ke liye)
@app.get("/api/workouts")
async def get_workouts():
    workouts = []
    async for workout in workout_collection.find():
        workouts.append(workout_helper(workout))
    return workouts

# Naya workout add karne ke liye (Sirf Admin ke liye UI mein set karenge)
@app.post("/api/workouts")
async def add_workout(workout_data: dict):
    new_workout = await workout_collection.insert_one(workout_data)
    created_workout = await workout_collection.find_one({"_id": new_workout.inserted_id})
    return workout_helper(created_workout)

# Workout delete karne ke liye
@app.delete("/api/workouts/{id}")
async def delete_workout(id: str):
    delete_result = await workout_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Workout delete ho gaya"}
    raise HTTPException(status_code=404, detail="Workout nahi mila")