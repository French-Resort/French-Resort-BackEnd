DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS guest CASCADE;
DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

CREATE TABLE IF NOT EXISTS "user" (
    id_user SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL UNIQUE,
	password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS guest (
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(30) NOT NULL
) INHERITS ("user");

CREATE TABLE IF NOT EXISTS room (
    id_room VARCHAR(50) PRIMARY KEY,
    room_type VARCHAR(50) NOT NULL,
    price_per_night MONEY NOT NULL,
    max_guests SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS booking (
    id_booking SERIAL PRIMARY KEY,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    id_room VARCHAR(50) NOT NULL,
    id_guest INTEGER NOT NULL,
    CONSTRAINT fk_room FOREIGN KEY (id_room) REFERENCES room (id_room),
    CONSTRAINT fk_guest FOREIGN KEY (id_guest) REFERENCES "user" (id_user)
);
