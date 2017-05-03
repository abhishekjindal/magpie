	const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/magpie';
const client = new pg.Client(connectionString);
client.connect();
const query = client.query(
  ' insert into users (email,password,name,usertype) values (\'ad@gmail.com\',\'qwert\',\'Paula Drake\',\'admin\');'
  +' insert into users (email,password,name,usertype) values (\'pat@gmail.com\',\'qwerty\',\'Pat Brown\',\'teacher\');'
  +' insert into users (email,password,name,usertype) values (\'shelly@gmail.com\',\'asdfg\',\'Shelly Bran\',\'teacher\');'
  +' insert into users (email,password,name,usertype) values (\'sara@gmail.com\',\'fghjkl\',\'Sara Brandon\',\'teacher\');'
  +' insert into users (email,password,name,usertype) values (\'karen@gmail.com\',\'fghjkl\',\'Karen Kelly\',\'parent\');'
  +' insert into users (email,password,name,usertype) values (\'sharon@gmail.com\',\'fghjkl\',\'Sharon Talor\',\'parent\');'
  +' insert into users (email,password,name,usertype) values (\'brad@gmail.com\',\'asdfghjkl\',\'Brad Talor\',\'parent\');'
  +' insert into users (email,password,name,usertype) values (\'hayden@gmail.com\',\'asdfghjkl\',\'Ross Hayden\',\'parent\');'

  +' insert into children values(1,\'Mat Talor\',6,\'09-03-2011\',\'lactose\');'
  +' insert into children values(2,\'Suzie Hayden\',6,\'09-05-2011\',\'gluten\');'
  +' insert into children values(3,\'James Kelly\',5,\'09-05-2012\',\'gluten\');'

  +'insert into parents values(5,3);'
  +'insert into parents values(6,1);'
  +'insert into parents values(8,2);'

  +'insert into classes values(1,\'blocks\',2);'
  +'insert into classes values(2,\'craft\',2);'
  +'insert into classes values(3,\'craft\',2);'

  +'insert into teachers values(1,1,1,23,\'gluten\',\'10-10-1994\');'
  +'insert into teachers values(2,1,1,23,\'gluten\',\'10-10-1994\');'
  +'insert into teachers values(2,2,1,23,\'gluten\',\'10-10-1994\');'
  +'insert into teachers values(2,3,1,23,\'gluten\',\'10-10-1994\');'
  +'insert into teachers values(3,1,1,23,\'gluten\',\'10-10-1994\');'
  +'insert into teachers values(3,2,1,23,\'gluten\',\'10-10-1994\');'
  +'insert into teachers values(3,3,1,23,\'gluten\',\'10-10-1994\');'
  );
query.on('end', () => { client.end(); });

