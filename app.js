
const express = require('express')
const app = express()
const port = 80

app.use(express.static('public'))

app.get('/latest', function (req, res) {
  shell('./latest.sh', function(result){
    res.send(result)
  })
})

app.get('/restart', function (req, res) {
  shell('./restart.sh', function(result){
    res.send(result)
  })
})

app.listen(port, () => {
  console.log(`Listening on port ${port}`)
})


function shell(command, callback) {
    const childfork = require('child_process');
    childfork.exec(command, function(error, stdout, stderr) {
        if (error !== null) {
            console.log(stderr)
            callback(stderr);
        } else {
            callback(stdout);
        }
    });
};
