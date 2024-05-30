# The Caffeinated Odyssey


https://github.com/princewillingoo/the_caffeinated_odyssey/assets/97766398/49d7c670-637f-41f0-912e-1078233b3c27


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
