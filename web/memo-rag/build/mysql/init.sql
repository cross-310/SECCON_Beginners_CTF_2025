CREATE DATABASE IF NOT EXISTS memodb
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE memodb;

CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(36) PRIMARY KEY,
  username VARCHAR(255) UNIQUE,
  password TEXT
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS memos (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36),
  body TEXT,
  visibility ENUM('public','private','secret') NOT NULL,
  password TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

INSERT IGNORE INTO users (id, username, password) VALUES
('069891c8-1d0a-4dad-8be5-87485aa647ec', 'admin', 'KEBbc6hMkQkkRALkLbs4VUjuPuSNVYdY');

INSERT IGNORE INTO memos (id, user_id, body, visibility, password) VALUES
('e8266120-835a-462e-9fcd-53c160394b9b', '069891c8-1d0a-4dad-8be5-87485aa647ec', 'ctf4b{b3_c4r3ful_0f_func710n_c4ll1n6_m15u53d_4rgum3nt5}', 'secret', 'SGuJ4DCZifBMZzZgHEQ3fV2bYDjJTmMq');