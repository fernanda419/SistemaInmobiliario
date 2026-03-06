CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role ENUM('admin','cliente') DEFAULT 'cliente'
);

CREATE TABLE lots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area INT,
    location VARCHAR(100),
    price DECIMAL(10,2),
    stage VARCHAR(50),
    status ENUM('disponible','reservado','vendido')
);

CREATE TABLE purchases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    lot_id INT,
    purchase_date DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(lot_id) REFERENCES lots(id)
);

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_id INT,
    amount DECIMAL(10,2),
    payment_date DATETIME,
    FOREIGN KEY(purchase_id) REFERENCES purchases(id)
);

CREATE TABLE pqrs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type VARCHAR(50),
    message TEXT,
    status VARCHAR(50),
    created_at DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id)
);