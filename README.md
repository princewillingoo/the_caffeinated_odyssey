# The Caffeinated Odyssey

1. Start Docker Compose

   ```bash
   docker compose up --build
   ```

2. Place an Order
  
   ```bash
   curl -X POST "http://localhost:5000/order/" -H "Content-Type: application/json" -d '{
    "client_name": "Prince Inyang",
    "coffee_type": "americano"
    }'
   ```

3. Start Processing Order
  
   ```bash
   curl -X GET http://localhost:5001/start/
   ```

4. Finish Processing Order
  
   ```bash
   curl -X POST "http://localhost:5001/finish/" -H "Content-Type: application/json" -d '{
    "order_id": 1
    }'
   ```
