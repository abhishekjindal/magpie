const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/todo';
const client = new pg.Client(connectionString);
client.connect();
const query = client.query(
  'CREATE TABLE login(id SERIAL PRIMARY KEY, email VARCHAR(40) not null, password VARCHAR(40) not null);');
query.on('end', () => { client.end(); });