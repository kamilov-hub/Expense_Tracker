DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE SEQUENCE users_id_seq AS SMALLINT;
CREATE SEQUENCE categories_id_seq AS SMALLINT;
CREATE SEQUENCE transactions_id_seq AS INTEGER;

CREATE TYPE users_role AS ENUM('user', 'admin');
CREATE TYPE categories_type AS ENUM('expense', 'income');

CREATE TABLE users(
	id SMALLINT DEFAULT nextval('users_id_seq'),
	first_name VARCHAR(100) NOT NULL,
	last_name VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	password_hash VARCHAR(255) NOT NULL,
	role users_role DEFAULT 'user',
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
ALTER TABLE users ADD CONSTRAINT users_id_pkey PRIMARY KEY(id);
ALTER TABLE users ADD CONSTRAINT users_email_ukey UNIQUE(email);

CREATE TABLE categories(
	id SMALLINT DEFAULT nextval('categories_id_seq'),
	name VARCHAR(100) NOT NULL,
	type categories_type NOT NULL,
	is_active BOOLEAN NOT NULL DEFAULT TRUE,
	created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE categories ADD CONSTRAINT categories_id_pkey PRIMARY KEY(id);
ALTER TABLE categories ADD CONSTRAINT categories_name_type_ukey UNIQUE(name, type);

CREATE TABLE transactions(
	id INTEGER DEFAULT nextval('transactions_id_seq'),
	user_id SMALLINT NOT NULL,
	category_id SMALLINT NOT NULL,
	amount NUMERIC(22, 4) NOT NULL,
	currency CHAR(3) NOT NULL,
	description TEXT,
	occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
	created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE transactions ADD CONSTRAINT transactions_id_pkey PRIMARY KEY(id);
ALTER TABLE transactions ADD CONSTRAINT transaction_user_id_fkey FOREIGN KEY(user_id) REFERENCES users(id);
ALTER TABLE transactions ADD CONSTRAINT transactions_category_id_fkey FOREIGN KEY(category_id) REFERENCES categories(id);
ALTER TABLE transactions ADD CONSTRAINT transactions_amount_check CHECK (amount > 0);