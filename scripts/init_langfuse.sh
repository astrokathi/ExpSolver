#!/bin/bash

# Wait for Langfuse to seed the default project
until psql -h db -U postgres -d langfuse -c "SELECT 1 FROM projects WHERE id='seed-project' LIMIT 1;" | grep -q 1; do
  echo "Waiting for Langfuse to seed the default organization and project..."
  sleep 3
done

echo "Database is ready. Injecting admin user..."

psql -h db -U postgres -d langfuse -c "
DO \$\$ 
BEGIN
  IF NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@test.com') THEN
    INSERT INTO users (id, email, password, admin) 
    VALUES ('admin_user_id', 'admin@test.com', '\$2a\$12\$qIipywAfajIQOhZPWFPVFuKbf9f/1Q3QDDFaXef4lL.PemDkzXnFy', true);
  END IF;
END \$\$;
"

echo "Assigning admin to Provisioned Org and Project..."

psql -h db -U postgres -d langfuse -c "
INSERT INTO organization_memberships (id, org_id, user_id, role) 
VALUES ('seeded_org_membership_admin', 'seed-org', 'admin_user_id', 'OWNER') 
ON CONFLICT DO NOTHING;
"

psql -h db -U postgres -d langfuse -c "
INSERT INTO project_memberships (project_id, user_id, org_membership_id, role) 
VALUES ('seed-project', 'admin_user_id', 'seeded_org_membership_admin', 'OWNER') 
ON CONFLICT DO NOTHING;
"

echo "Admin initialization complete."
