DROP TABLE IF EXISTS USERS CASCADE;
DROP TABLE IF EXISTS POST CASCADE;
DROP TABLE IF EXISTS POST_OPINION CASCADE;
DROP TABLE IF EXISTS COMMENT_OPINION CASCADE;
DROP TABLE IF EXISTS COMMENT CASCADE;
DROP TABLE IF EXISTS ANNOTATION CASCADE;


-- To generate unique ID's for posts
CREATE EXTENSION "uuid-ossp";

-- Can make some funnier random name generation
CREATE FUNCTION DEFAULT_NAME() RETURNS VARCHAR(255) AS $$
    SELECT 'smith';
$$ LANGUAGE SQL;

-- USER is a reserved keyword
CREATE TABLE USERS (
    ID UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
    -- Unique ID for user

    NAME VARCHAR(255) DEFAULT DEFAULT_NAME(),
    -- Name of user

    PW_HASH VARCHAR(255),
    -- Hashed password

    EMAIL VARCHAR(255) UNIQUE,
    -- Email of user

    TOKEN TEXT,
    -- Session Token

    LAST_LOGIN DATE
    -- To remove if it's a temp user after inactivity.
);

CREATE TABLE POST (
    ID UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
    -- Id of post

    TIME DATE NOT NULL,
    -- Time of Creation

    TITLE TEXT NOT NULL,
    -- Post Title

    CONTENT JSONB NOT NULL,
    -- POSTGRESS SUPPORTS STORING JSON

    OWNER UUID REFERENCES users (id)
    -- Owner of Post
);

CREATE TABLE COMMENT (
  ID SERIAL PRIMARY KEY,
  -- Unique identifier

  TARGET_POST UUID REFERENCES post (id),
  -- Post comment belongs to

  PARENT INTEGER REFERENCES COMMENT (id),
  -- Post parent (Optional)

  OWNER UUID REFERENCES users (id),
  -- UUID of the holder

  CONTENT JSONB NOT NULL,
  -- Content of comment

  TIME DATE NOT NULL
);

CREATE TABLE COMMENT_OPINION (
  TARGET INTEGER REFERENCES comment (id),
  -- UUID of whatever it belongs to.

  OWNER UUID REFERENCES users (id),
  -- UUID of the holder

  STATE BOOLEAN NOT NULL,
  -- Opinion

  PRIMARY KEY(TARGET, OWNER)
  -- So that you cant like multiple times
);

CREATE TABLE POST_OPINION (
  TARGET UUID REFERENCES post (id),
  -- UUID of whatever it belongs to.

  OWNER UUID REFERENCES users (id),
  -- UUID of the holder

  STATE BOOLEAN NOT NULL,
  -- Opinion

  PRIMARY KEY(TARGET, OWNER)
  -- So that you cant like multiple times
);

CREATE TABLE ANNOTATION (
  ID SERIAL PRIMARY KEY,
  -- Unique identifier

  TARGET_POST UUID REFERENCES post (id),
  -- What post it belongs to

  TARGET_COMMENT INTEGER REFERENCES comment (id),
  -- What comment it belongs to

  BEGINING INTEGER NOT NULL,
  -- Begining of annotation

  ENDING INTEGER NOT NULL,
  -- Ending of annotation

  COLOR VARCHAR(255)
  -- Hexadecimal color of Annotation (Might be fun?)
);

CREATE USER DELTA WITH PASSWORD '012';

GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA public 
TO delta;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO delta;

-- Add and revoke priveleges here later
