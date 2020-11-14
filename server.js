/*websocket通信*/
/*与小程序通信*/
var ws = require("nodejs-websocket");
console.log("开始建立连接...")

var fs=require('fs');
var file="C://Users/jimaz/Desktop/project/data/json/communicate.json";
var config=JSON.parse(fs.readFileSync(file));
var person_info=config['person'];
var time_info=config['time'];

var server = ws.createServer(function(conn){
    conn.on("text", function (str) {
        console.log("收到的信息为:"+str)
        if(str=="getpersons")
		{
			conn.sendText(person_info)
		}
		else
		{
			conn.sendText(time_info)
		}
    })
    conn.on("close", function (code, reason) {
        console.log("关闭连接")
    });
    conn.on("error", function (code, reason) {
        console.log("异常关闭")
    });
}).listen(8001)


console.log("WebSocket建立完毕")