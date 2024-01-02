DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS guest CASCADE;
DROP TABLE IF EXISTS room CASCADE;
DROP TABLE IF EXISTS admin CASCADE;

CREATE TABLE admin(
   id_admin SERIAL,
   email VARCHAR(50) NOT NULL,
   password TEXT NOT NULL,
   PRIMARY KEY(id_admin),
   UNIQUE(email)
);

CREATE TABLE guest(
   id_guest SERIAL,
   first_name VARCHAR(50) NOT NULL,
   last_name VARCHAR(50) NOT NULL,
   phone_number VARCHAR(30) NOT NULL,
   email VARCHAR(50) NOT NULL,
   password TEXT NOT NULL,
   PRIMARY KEY(id_guest),
   UNIQUE(phone_number),
   UNIQUE(email)
);

CREATE TABLE room(
   id_room VARCHAR(50),
   price_per_night NUMERIC(10,2) NOT NULL,
   max_guests SMALLINT NOT NULL,
   room_type VARCHAR(50) NOT NULL,
   PRIMARY KEY(id_room)
);

CREATE TABLE booking(
   id_booking SERIAL,
   check_in_date DATE NOT NULL,
   check_out_date DATE NOT NULL,
   total_price NUMERIC(10,2),
   id_room VARCHAR(50) NOT NULL,
   id_guest INTEGER NOT NULL,
   PRIMARY KEY(id_booking),
   FOREIGN KEY(id_room) REFERENCES room(id_room),
   FOREIGN KEY(id_guest) REFERENCES guest(id_guest)
);
