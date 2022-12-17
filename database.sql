create table customer(
    cust_id serial primary key,
    full_name text,
    gender text,
    email text unique,
    address text,
    telephone text,
    payment_method text,
    username text
);

create table trip(
    trip_id serial primary key,
    pickup_address text,
    drop_off_address text,
    pickup_date date,
    pickup_time time,
    trip_status text,
    payment_status text,
    driver_id int,
    cust_id int
);

create table driver(
    driver_id serial primary key,
    full_name text,
    gender text,
    license_id text unique,
    username text
);

create table admin(
    admin_id serial primary key,
    full_name text,
    gender text,
    username text
);

create table credentials(
    username text primary key,
    user_password text,
    user_role text
);
