-- INSERT INTO "user"(email, password_hash, role) VALUES
('admin@demo.local', '$pbkdf2-sha256$29000$YgGgUoY4muRrA3sIvvI3rA$zWqEwIyp0jZQYvS6nWl.5VxJ2QZfDEd4s6GkZ1Kq4Z0', 'admin')
ON CONFLICT (email) DO NOTHING;

-- balances & accounts will be created by app seeds as well
