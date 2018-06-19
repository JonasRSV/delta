DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS POST;
DROP TABLE IF EXISTS OPINION;
DROP TABLE IF EXISTS COMMENT;
DROP TABLE IF EXISTS ANNOTATION;

-- To generate unique ID's for posts
CREATE EXTENSION "uuid-ossp";

-- Can make some funnier random name generation
CREATE FUNCTION DEFAULT_NAME() RETURNS VARCHAR(255) AS $$
    SELECT 'smith';
$$ LANGUAGE SQL;

-- USER is a reserved keyword
CREATE TABLE USERS (
    ID UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
    NAME VARCHAR(255) DEFAULT DEFAULT_NAME(),
    PW_HASH VARCHAR(255),
    EMAIL VARCHAR(255),

    -- To remove if it's a temp user after inactivity.
    LAST_LOGIN DATE
);

CREATE TABLE POST (
    ID UUID PRIMARY KEY,
    TIME DATE NOT NULL,
    TITLE TEXT NOT NULL,

    -- POSTGRESS SUPPORTS STORING JSON
    CONTENT JSONB NOT NULL,

    OWNER UUID REFERENCES users (id)
);


CREATE TABLE OPINION (
  ID SERIAL PRIMARY KEY,
  -- Unique identifier

  TARGET UUID,
  -- UUID of whatever it belongs to.

  BELONG SMALLINT,
  -- IDENTIFIER OF TYPE IT BELONGS TO

  OWNER UUID REFERENCES users (id),
  -- UUID of the holder

  STATE BOOLEAN NOT NULL,
  -- Opinion

  TIME DATE NOT NULL
);

CREATE TABLE COMMENT (
  ID SERIAL PRIMARY KEY,
  -- Unique identifier

  TARGET UUID,
  -- UUID of whatever it belongs to.

  BELONG SMALLINT,
  -- IDENTIFIER OF TYPE IT BELONGS TO

  OWNER UUID REFERENCES users (id),
  -- UUID of the holder

  CONTENT JSONB NOT NULL,
  -- Content of comment

  TIME DATE NOT NULL
);

CREATE TABLE ANNOTATION (
  ID SERIAL PRIMARY KEY,
  -- Unique identifier

  TARGET UUID REFERENCES post (id),
  -- What post it belongs to

  BEGINING INTEGER NOT NULL,
  -- Begining of annotation

  ENDING INTEGER NOT NULL,
  -- Ending of annotation

  COLOR VARCHAR(255)
  -- Hexadecimal color of Annotation (Might be fun?)
);

CREATE USER DELTA WITH PASSWORD '012';

-- Add and revoke priveleges here later
