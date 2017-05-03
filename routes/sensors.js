const express = require('express');
const router = express.Router();
const fs = require('fs');
const date = new Date;

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

router.get('/dismissal', function(req,res){
    const results = [];
    const query = client.query('SELECT * FROM dismissal;');
    query.on('row', (row) => {
         results.push(row);
    });
    query.on('end', () => {
        res.send(results);
    });
});

router.post('/dismissal', function(request, respond) {
    var body = '';
    filePath = __dirname + '/sensors/';
    const results = [];
    var childname = '';
    //console.log(request.files);

    
    request.on('data', function(data) {
        //var obj = JSON.parse(data);
        body += data;
        console.log(body);
        parameters = body.split('&');
        console.log(parameters);
        date = (parameters[0].split('='))[1];
        time = (parameters[2].split('='))[1];
        id = (parameters[1].split('='))[1];
        //id_int = parseInt(id,10);
          pg.connect(connectionString, (err, client, done) => {
            // Handle connection errors
            if(err) {
              done();
              console.log(err);
              return res.status(500).json({success: false, data: err});
            }
    
            const query = client.query('SELECT child_id FROM sensors WHERE node_id=($1)',[id]);
            child_id_int = -1;
            query.on('row', (row) => {
               child_id_int = parseInt(row.child_id,10);
            });
            query.on('end', () => {
                done();
                const query1 = client.query('SELECT * FROM children WHERE child_id=($1)',[child_id_int]);

                query1.on('row', (row) => {
                    childname = row.name;
                    results.push(row);
                    console.log(childname);

                });
                query1.on('end', () => { 
                  done();
                  const query2 = client.query('INSERT INTO dismissal(name) VALUES($1);',[childname])
                });

            });
            


          });


    });
    
    request.on('end', function (){
        //console.log(body);
        respond.send("received");
    });

    
});


module.exports = router;