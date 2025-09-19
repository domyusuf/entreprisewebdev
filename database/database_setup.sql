-- Create database
CREATE DATABASE IF NOT EXISTS momo_sms_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;
USE momo_sms_db;

-- Users table
CREATE TABLE IF NOT EXISTS Users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(191) NOT NULL,
  phone_number VARCHAR(50) UNIQUE,
  account_balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
  account_type ENUM('personal','business','savings','checking') NOT NULL DEFAULT 'personal',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Transactions table
CREATE TABLE IF NOT EXISTS Transactions (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  external_transaction_id VARCHAR(191) UNIQUE,
  type ENUM('credit','debit','transfer','topup','withdrawal','refund','fee') NOT NULL,
  body TEXT,
  amount DECIMAL(15,2) NOT NULL,
  sender_id INT UNSIGNED NULL,
  receiver_id INT UNSIGNED NULL,
  service_center VARCHAR(191),
  date_sent DATETIME,
  balance_after DECIMAL(15,2),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_transactions_sender_id (sender_id),
  INDEX idx_transactions_receiver_id (receiver_id),
  CONSTRAINT fk_transactions_sender FOREIGN KEY (sender_id) REFERENCES users(id)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_transactions_receiver FOREIGN KEY (receiver_id) REFERENCES users(id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- System logs table
CREATE TABLE IF NOT EXISTS System_Logs (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  transaction_id INT UNSIGNED NULL,
  level ENUM('debug','info','warning','error','critical') NOT NULL DEFAULT 'info',
  message TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_system_logs_transaction_id (transaction_id),
  CONSTRAINT fk_system_logs_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Transaction categories table
CREATE TABLE IF NOT EXISTS Transaction_Categories (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(191) NOT NULL UNIQUE,
  description TEXT,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Transaction <-> Category assignment (many-to-many)
CREATE TABLE IF NOT EXISTS Transaction_Category_Assignment (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  transaction_id INT UNSIGNED NOT NULL,
  transaction_category_id INT UNSIGNED NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_tca_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_tca_category FOREIGN KEY (transaction_category_id) REFERENCES Transaction_Categories(id)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  UNIQUE KEY uniq_transaction_category (transaction_id, transaction_category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
