INSERT INTO "permissions" (name, codename) VALUES
    ('Read me', 'read_me'),
    ('Update me', 'update_me'),
    ('Delete me', 'delete_me'),
    ('Register user', 'new_user'),
    ('Add permissions', 'add_permission'),
    ('Remove permissions', 'remove_permissions');

INSERT INTO "users" (username, email) VALUES ('admin', 'admin@gmail.com');

INSERT INTO "permission_user" (user_id, permission_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5);
