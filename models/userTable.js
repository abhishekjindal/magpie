const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/todo';
const client = new pg.Client(connectionString);
client.connect();
const query = client.query(
	'CREATE TYPE usertype AS ENUM(\'admin\', \'teacher\', \'parent\');'
  +'CREATE TABLE IF NOT EXISTS users('
  +'id SERIAL PRIMARY KEY,'
  +' email VARCHAR(30) not null,'
  +' password VARCHAR(20) not null,'
  +' name VARCHAR(30) not null,'
  +' usertype usertype);'
  );
query.on('end', () => { client.end(); });