const express = require('express');
const router = express.Router();
const path = require('path');
var local = {};
var query = "";


/* GET home page. */


router.get('/user/*', function(req, res, next){
	local = {
		userid : req.session.row_id,
		type : req.session.type,
		query : req.query.option,
		id : req.query.id
	};

	// console.log(req.query.option);
	
	// console.log(local.type);
 	// res.render(req.path.split('/')[1], local);
 	res.render(path.resolve("views" +req.path), local);
 });

 router.get('/*', function(req, res, next) {
   res.render(req.path.split('/')[1]);
 });

 




module.exports = router;
