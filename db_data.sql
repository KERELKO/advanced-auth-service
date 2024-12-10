-- Insert into "permissions"
INSERT INTO "permissions" (name, codename) VALUES
    ('Read me', 'read_me'),
    ('Update me', 'update_me'),
    ('Delete me', 'delete_me'),
    ('Register user', 'new_user'),
    ('Add permissions', 'add_permission'),
    ('Remove permissions', 'remove_permissions')
ON CONFLICT (codename) DO NOTHING;

-- Insert into "users"
INSERT INTO "users" (username, email) VALUES
    ('admin', 'admin@gmail.com')
ON CONFLICT (username) DO NOTHING;

-- Insert into "permission_user"
INSERT INTO "permission_user" (user_id, permission_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5)
ON CONFLICT DO NOTHING;
