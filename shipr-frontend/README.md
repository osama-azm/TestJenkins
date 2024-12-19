# Shipr 🚢

Shipr is a personal project aimed at helping folks understand distributed microservice architecture. It’s a simple, lightweight system designed to manage products, process orders, and handle payments.

## Shipr frontend

The frontend repository for the Shipr project.

- **Products (`/`)**: Endpoint to add products.

- **Orders (`/orders`)**: Endpoint to place orders.

## Architecture

![Shipr Architecture](./shipr-architecture.png)

## Getting Started

### Prerequisites

- Node.js
- npm

### Running project

1. Install packages 
    ```bash
    npm install
    ```
2. Make sure you have a .env file with following variables.
    ```
    REACT_APP_INVENTORY_SERVICE_URL=xxx
    REACT_APP_PAYMENTS_SERVICE_URL=xxx
    ```
3. Run frontend locally
   ```bash
   npm start
   ```