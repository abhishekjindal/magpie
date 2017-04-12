const express = require('express');
const router = express.Router();
const path = require('path');
var user = {};


/* GET home page. */

router.get('/', function(req, res, next) {
  res.render("index");
});

router.get('/user/*', function(req, res, next){
	local = {
		userid : req.session.row_id,
		type : req.session.type
	};
	// console.log(local.type);
 	res.render(req.path.split('/')[1], local);
 });

 router.get('/*', function(req, res, next) {
   res.render(req.path.split('/')[1]);
 });

 




module.exports = router;
