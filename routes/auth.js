const express = require('express');
const router = express.Router();
const pg = require('pg');
const path = require('path');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/todo';

client = {};
pg.connect(connectionString, (err, thisclient, done) => {
	client = thisclient;
})

router.get('/', function(req, res, next) {
	res.send("you are accessing home auth")
})

router.get('/registersuccess', function(req, res, next) {
	res.send("successfully signed up");
});

router.post('/register', function(req, res, next) {
	const email = req.body.email;
	const password = req.body.password;
    // SQL Query > Insert Data
	client.query('INSERT INTO login(email, password) values($1, $2);',[email, password]);
	// Response
    res.writeHead(301,{
		"Location" : "registersuccess"
	});
	res.end();
});

router.get('/loginsuccess', function(req, res, next) {
	res.send("successfully logged in");
});

router.post('/login', function(req, res, next) {
	const email = req.body.email;
	const password = req.body.password;
	var loginsuccess = false;
	 
    query = client.query('SELECT * FROM users where email=\''+email+'\';');

    query.on('row', (row) => {
    	if(password == row.password){
    		loginsuccess = true;
    		req.session.row_id = row.id;
    		req.session.type = row.usertype;

    	}else{
    		res.send("password does not match");
    	}
    });
    

    query.on('end', () => {
    	if (!loginsuccess) {
      		res.send("username does not exist");
      	}else{
      		req.session.loggedin = true; 		
      		res.redirect('/user/index');
      	}
    });

});

router.post('/logout', function(req, res, next){
	req.session.destroy(function(err) {
	  if(err) {
	    console.log(err);
	  } else {
	    res.redirect('/');
	  }
	});
});

module.exports = router;