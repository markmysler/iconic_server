from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from google.cloud import firestore

router = APIRouter()

# Initialize Firestore client
# fs = firestore.Client()

connected_users = {}

async def update_firestore_on_disconnect(user_id: str):
    """Update Firestore to mark the user as disconnected."""
    # user_ref = fs.collection("users").document(user_id)
    # user_ref.update({"status": "offline"})
    print("desconectado")

@router.websocket("")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    # Accept the connection
    await websocket.accept()
    connected_users[user_id] = websocket
    print(f"User {user_id} connected")

    try:
        # Keep the connection alive
        while True:
            await websocket.receive_text()  # This will block and keep the connection open
    except WebSocketDisconnect:
        # Handle disconnection
        del connected_users[user_id]
        print(f"User {user_id} disconnected")
        await update_firestore_on_disconnect(user_id)
