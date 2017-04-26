const express = require('express');
const router = express.Router();
const pg = require('pg');
const path = require('path');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/magpie';
var local = {};

client = {};
pg.connect(connectionString, (err, thisclient, done) => {
	client = thisclient;
})
/* GET users listing. */

router.get('/students', function(req, res, next) {

	const children = [];

	const query = client.query('select * from children');
    // Stream results back one row at a time
    query.on('row', (row) => {
      children.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : req.query.option,
		children : children
	};
      res.render('user/admin/students', local);
    });
  
});

router.get('/getstudent', function(req, res, next) {

	const child = [];
	const id = req.query.id;
	const query = client.query('select * from children where child_id=\''+id+'\'');
    // Stream results back one row at a time
    query.on('row', (row) => {
      child.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : "student",
		id : id,
		child : child
	};
      res.render('user/admin/students', local);
    });
  
});

router.get('/teachers', function(req, res, next) {

	const teachers = [];

	const query = client.query('select * from teachers');
    // Stream results back one row at a time
    query.on('row', (row) => {
      teachers.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : req.query.option,
		teachers : teachers
	};
      res.render('user/admin/teachers', local);
    });
  
});

router.get('/geteacher', function(req, res, next) {

	const teacher = [];
	const id = req.query.id;
	const query = client.query('select * from teachers where user_id=\''+id+'\'');
    // Stream results back one row at a time
    query.on('row', (row) => {
      teacher.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : "teacher",
		id : id,
		teacher : teacher
	};
      res.render('user/admin/teachers', local);
    });
  
});

router.get('/admins', function(req, res, next) {

	const admins = [];

	const query = client.query('select * from users where usertype=\'admin\'');
    // Stream results back one row at a time
    query.on('row', (row) => {
      admins.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : req.query.option,
		admins : admins
	};
      res.render('user/admin/admins', local);
    });
  
});

router.get('/getadmin', function(req, res, next) {

	const admin = [];
	const id = req.query.id;
	const query = client.query('select * from users where id=\''+id+'\'');
    // Stream results back one row at a time
    query.on('row', (row) => {
      admin.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : "admin",
		id : id,
		admin : admin
	};
      res.render('user/admin/admins', local);
    });
  
});

router.get('/classes', function(req, res, next) {

	const classes = [];

	const query = client.query('select * from classes');
    // Stream results back one row at a time
    query.on('row', (row) => {
      classes.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : req.query.option,
		classes : classes
	};
      res.render('user/admin/classes', local);
    });
  
});

router.get('/getclass', function(req, res, next) {

	const classview = [];
	const id = req.query.id;
	const query = client.query('select * from classes where class_id=\''+id+'\'');
    // Stream results back one row at a time
    query.on('row', (row) => {
      classview.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
    	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : "classview",
		id : id,
		classview : classview
	};
      res.render('user/admin/classes', local);
    });
  
});



module.exports = router;
