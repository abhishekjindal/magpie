const express = require('express');
const router = express.Router();
const fs = require('fs');
const pg = require('pg');
const connectionString = process.env.DATABASE_URL || 'postgres://localhost:5432/magpie';
const date = new Date;

client = {};
pg.connect(connectionString, (err, thisclient, done) => {
    client = thisclient;
})

router.post('/receive', function(request, respond) {
    var body = '';
    filePath = __dirname + '/sensors/';
    console.log(request.body.data);
    console.log(request.files);

    
    request.on('data', function(data) {
        body += data;
    });

    request.on('end', function (){

    	fs.writeFile('activities_'+date+'.csv', body, function() {
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
 
    request.on('data', function(data) {
        body += data;
        console.log(body);
        parameters = body.split('&');
        console.log(parameters);
        date = (parameters[0].split('='))[1];
        time = (parameters[2].split('='))[1];
        id = (parameters[1].split('='))[1];
        const query = client.query('SELECT child_id FROM sensors WHERE node_id=($1)',[id]);
        child_id_int = -1;
        query.on('row', (row) => {
           child_id_int = parseInt(row.child_id,10);
        });
        query.on('end', () => {
            const query1 = client.query('SELECT * FROM children WHERE child_id=($1)',[child_id_int]);

            query1.on('row', (row) => {
                childname = row.name;
                results.push(row);
                console.log(childname);

            });
            query1.on('end', () => { 
              const query2 = client.query('INSERT INTO dismissal(name) VALUES($1);',[childname])
            });
        });
    });
    
    request.on('end', function (){
        respond.send("received");
    });
});


module.exports = router;