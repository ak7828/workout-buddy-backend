from motor.motor_asyncio import AsyncIOMotorClient

# Local MongoDB connection URL
MONGO_DETAILS = "mongodb://localhost:27017"

# Client aur database setup karein
client = AsyncIOMotorClient(MONGO_DETAILS)

# Aapke database ka naam "workout_buddy" rakha hai
database = client.workout_buddy 

# Collections (Tables) jahan data save hoga
workout_collection = database.get_collection("workouts")
user_collection = database.get_collection("users")