// lex.js
var AWS = require('aws-sdk'),
   fs = require('fs'),
   ts = require('tailstream'),
   exec = require('child_process').exec;

   var FULFILLED = 'Fulfilled',
   RESPONSE_FILE = 'response.mpeg',
   REMOVE_REQUEST_FILE = 'rm request.wav',
   SOX_COMMAND = 'sox -d -t wavpcm -c 1 -b 8 -r 16000 -e signed-integer --endian little - silence 1 0 1% 5 0.3t 2% > request.wav',
   streaming = false,
   inputStream,
   lexruntime = new AWS.LexRuntime({
     region: 'us-east-1',
     credentials: new AWS.Credentials(
       'AKIAJ7LPTTXWB7KLSHDQ',
       'k8bSLsUk+jp8N8Q9fSlKUBe3vg3IMfBc2Sd+Q1Yz', null)
   });

var setupStream = function() {
   streaming = true;
   inputStream = ts.createReadStream('./request.wav');
   var params = {
     botAlias: '$LATEST',
     botName: 'ApplianceManager',
     userId: 'lexHeadTesting',
     contentType: 'audio/l16; rate=16000; channels=1',
     inputStream: inputStream
   };

   lexruntime.postContent(params, function(err, data) {
     if (err) {
       console.log(err, err.stack);
       process.exit(1);
     } else {
       fs.writeFile(RESPONSE_FILE, data.audioStream, function(err) {
         if (err) {
           return console.log(err);
           process.exit(1);
         }
       });
       var playback = exec('mpg321 ' + RESPONSE_FILE, function(error, stdout,stderr){
       if(error)
       {
           console.error('error:' + error);
           return;
       }
       console.log('stdout:' + stdout);
       console.log('stderr' + typeof stderr);
   });
       playback.on('close', function(code) {
           exec('rm ' + RESPONSE_FILE);
           if (data.dialogState !== FULFILLED) {
             streaming = false;
             record();
           }
         });
       }
   });
 }

var record = function() {
   exec('mpg321 resources/ding.mp3', function(error, stdout, stderr){
       if(error)
       {
           console.log('error ', error);
           return;
       }
       else
       {
	  console.log(stdout);
          console.log(stderr);
       }
   });
   setTimeout(function(){
   var recording = exec(SOX_COMMAND);
   recording.stderr.on('data', function(data) {
     console.log(data);
     if (!streaming) {
       setupStream();
     }
   });
   recording.on('close', function(code) {
     inputStream.done();
     exec(REMOVE_REQUEST_FILE);
   });
},500);
 }
record();
