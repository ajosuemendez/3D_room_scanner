// Connecting to ROS
  // -----------------
  window.onload = doStuff;

  

  var ros = new ROSLIB.Ros({
    url : 'ws://localhost:9090'
  });

  ros.on('connection', function() {
    console.log('Connected to websocket server.');
  });

  ros.on('error', function(error) {
    console.log('Error connecting to websocket server: ', error);
  });

  ros.on('close', function() {
    console.log('Connection to websocket server closed.');
  });

  // Publishing a Topic
  // ------------------

 var startCommand = new ROSLIB.Topic({
    ros : ros,
    name : '/start_cmd',
    messageType : 'std_msgs/String'
 });

  function doStuff(){
    if (localStorage.getItem("initBtn") === "disable") {
      console.log(localStorage.getItem("initBtn") === "disable");
      const initBtn = document.getElementById("btn-init");
      const startBtn = document.getElementById("btn-start");
  
      console.log("adding disable to init");
      console.log("removing disable to start");
  
      
      initBtn.classList.add("disable");
      console.log(initBtn);
  
      startBtn.classList.remove("disable");
      console.log(startBtn);
  
    };
  }

  

  //localStorage.removeItem("initBtn");


  function startHandler(event) {
    const initBtn = document.getElementById("btn-init");
    const startBtn = document.getElementById("btn-start");
    const stopBtn = document.getElementById("btn-stop");
    const killBtn = document.getElementById("btn-kill");


    const pressedBtn = `${event.target.getAttribute("name")}`
    console.log(pressedBtn);

    var startMessage = new ROSLIB.Message({
      data : pressedBtn
    });
    startCommand.publish(startMessage);

    if(pressedBtn === "stop"){
      window.location.reload();
    }

  };

  

  // Subscribing to a Topic
  // ----------------------

  // var listener = new ROSLIB.Topic({
  //   ros : ros,
  //   name : '/listener',
  //   messageType : 'std_msgs/String'
  // });
  //
  // listener.subscribe(function(message) {
  //   console.log('Received message on ' + listener.name + ': ' + message.data);
  //   listener.unsubscribe();
  // });
  //
  // // Calling a service
  // // -----------------
  //
  // var addTwoIntsClient = new ROSLIB.Service({
  //   ros : ros,
  //   name : '/add_two_ints',
  //   serviceType : 'rospy_tutorials/AddTwoInts'
  // });
  //
  // var request = new ROSLIB.ServiceRequest({
  //   a : 1,
  //   b : 2
  // });
  //
  // addTwoIntsClient.callService(request, function(result) {
  //   console.log('Result for service call on '
  //     + addTwoIntsClient.name
  //     + ': '
  //     + result.sum);
  // });
  //
  // // Getting and setting a param value
  // // ---------------------------------
  //
  // ros.getParams(function(params) {
  //   console.log(params);
  // });
  //
  // var maxVelX = new ROSLIB.Param({
  //   ros : ros,
  //   name : 'max_vel_y'
  // });
  //
  // maxVelX.set(0.8);
  // maxVelX.get(function(value) {
  //   console.log('MAX VAL: ' + value);
  // });
