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
  
  +'CREATE TABLE IF NOT EXISTS children('
  +'child_id INT not null,'
  +'name VARCHAR(30) not null,'
  +'age INT not null,'
  +'birthday DATE not null,'
  +'allergies VARCHAR(30),'
  +'PRIMARY KEY(child_id));'

  +'CREATE TABLE IF NOT EXISTS dismissal('
  +'id INT not null,'
  +'name VARCHAR(30) not null);'
  
  
  +'CREATE TABLE IF NOT EXISTS sensors('
  +'node_id VARCHAR(50) not null,'
  +'timestamp TIMESTAMP not null default now(),'
  +'child_id INT not null,'
  +'input_flag BOOL not null,'
  +'type VARCHAR(20) not null,'
  +'PRIMARY KEY(node_id,child_id, timestamp),'
  +'FOREIGN KEY (child_id) REFERENCES children(child_id) ON DELETE CASCADE);'

  +'CREATE TABLE IF NOT EXISTS parents('
  +'user_id  INT,'
  +'child_id INT,' 
  +'PRIMARY KEY (user_id, child_id),' 
  +'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,'
  +'FOREIGN KEY(child_id) REFERENCES children(child_id) ON DELETE CASCADE);'

  +'CREATE TABLE IF NOT EXISTS classes('
  +'class_id INT NOT NULL UNIQUE,' 
  +'activity_name VARCHAR(30) not null,'
  +'activity_id INT not null,'
  +'PRIMARY KEY(class_id) );'

  +'CREATE TABLE IF NOT EXISTS teachers('
  +'user_id INT NOT NULL,'
  +'child_id INT NOT NULL,'
  +'class_id INT NOT NULL,'
  +'age INT not null,'
  +'allergies VARCHAR(30) not null,'
  +'birthday DATE not null,'
  +'PRIMARY KEY (user_id, child_id, class_id),'
  +'FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,'
  +'FOREIGN KEY(child_id) REFERENCES children(child_id) ON DELETE CASCADE,'
  +'FOREIGN KEY(class_id) REFERENCES classes(class_id) ON DELETE CASCADE);'
	);
query.on('end', () => { client.end(); });