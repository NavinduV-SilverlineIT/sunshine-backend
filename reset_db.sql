-- Drop existing tables if they exist
DROP TABLE IF EXISTS vehicle_parts_vehicleparts_saleitems CASCADE;
DROP TABLE IF EXISTS vehicle_parts_vehicleparts_sales CASCADE;
DROP TABLE IF EXISTS vehicle_parts_vehicleparts_purchases CASCADE;
DROP TABLE IF EXISTS vehicle_parts_vehicleparts CASCADE;
DROP TABLE IF EXISTS vehicle_parts_vehicle CASCADE;

-- Drop all Django related tables
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS authtoken_token CASCADE;
DROP TABLE IF EXISTS authtoken_tokenproxy CASCADE; 