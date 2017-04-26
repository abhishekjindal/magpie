	const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/magpie';
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
  +' insert into users (email,password,name,usertype) values (\'admin\',\'admin\',\'admin\',\'admin\');'
  +' insert into users (email,password,name,usertype) values (\'par\',\'par\',\'par\',\'parent\');'
  +' insert into users (email,password,name,usertype) values (\'teach\',\'teach\',\'teach\',\'teacher\');'
  );
query.on('end', () => { client.end(); });

