.headers on
.mode columns

CREATE TABLE IF NOT EXISTS users (
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    );

--username:admin,password:1234
--username:user,password:4321
INSERT INTO users(username,name,password) VALUES
('admin','Administrador del sistema','7110eda4d09e062aa5e4a390b0a572ac0d2c0220'),
('user','Usuario del sistema','d5f12e53a182c062b6bf30c1445153faff12269a');

SELECT * FROM users;