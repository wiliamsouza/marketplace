#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE product;
    CREATE DATABASE test_product;
    CREATE DATABASE test_promotion;
    GRANT ALL PRIVILEGES ON DATABASE product TO postgres;
    GRANT ALL PRIVILEGES ON DATABASE test_product TO postgres;
    GRANT ALL PRIVILEGES ON DATABASE test_promotion TO postgres;
EOSQL
