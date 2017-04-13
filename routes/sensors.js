const express = require('express');
const router = express.Router();
const fs = require('fs');

router.get('/receive',function(req, res){
	res.send('listening');
});

router.post('/receive', function(request, respond) {
    var body = '';
    filePath = __dirname + '/sensors/';
    console.log(request.body.data);
    console.log(request.files);

    
    request.on('data', function(data) {
    	//var obj = JSON.parse(data);
        body += data;
    });

    request.on('end', function (){

    	fs.writeFile('logfile2.csv', body, function() {
            respond.end();
        });
    });

    respond.send("received");
});


module.exports = router;