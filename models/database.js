const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/magpie';
const client = new pg.Client(connectionString);
client.connect();
const query = client.query(
  'CREATE TABLE IF NOT EXISTS parents('
	+'user_id SERIAL PRIMARY KEY,'
	+'age SERIAL not null,'
	+'allergies VARCHAR(30) not null,'
	+'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);'

+'CREATE TABLE IF NOT EXISTS teachers('
	+'user_id SERIAL PRIMARY KEY,'
	+'name VARCHAR(30) not null,'
	+'age SERIAL not null,'
	+'allergies VARCHAR(30) not null,'
	+'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);'

+'CREATE TABLE IF NOT EXISTS users('
  +'id SERIAL PRIMARY KEY,'
  +'email VARCHAR(30) not null,'
  +'password VARCHAR(20) not null,'
  +'name VARCHAR(30) not null,'
  +'usertype usertype);'

+'CREATE TABLE IF NOT EXISTS children('
  +'child_id SERIAL PRIMARY KEY,'
  +'name VARCHAR(30) not null);'


+'CREATE TABLE IF NOT EXISTS classes('
  +'class_id SERIAL PRIMARY KEY,'
  +'name VARCHAR(30) not null);'

+'CREATE TABLE IF NOT EXISTS child_teacher_class('
	+'child_id integer not null,'
	+'class_id integer not null,'
	+'user_id integer not null,'
	+'PRIMARY KEY(child_id,class_id,user_id),'
	+'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,'
	+'FOREIGN KEY(child_id) REFERENCES children(child_id) ON DELETE CASCADE,'
	+'FOREIGN KEY(class_id) REFERENCES classes(class_id) ON DELETE CASCADE);'
	);
query.on('end', () => { client.end(); });