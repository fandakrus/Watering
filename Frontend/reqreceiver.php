<?php
    function OpenDbCon() {
        $servername = getenv('DB_SERVER');
        $username = getenv('DB_USER');
        $password = getenv('DB_PASSWD');
        $dbname = getenv('DB_NAME');
        // Create connection 
        $conn = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: ". $conn->connect_error);
        }

        return $conn;
    }

    // open object with database connection
    $conn = OpenDbCon();


    if(isset($_GET['changed'])) {
        $circle1=$_GET['circle1'];
        $circle2=$_GET['circle2'];
        $circle3=$_GET['circle3'];
        $circle4=$_GET['circle4'];
        $main_control=$_GET['main-control'];
        $water_source=$_GET['water-source'];
    }
    
    
    $sql = "INSERT INTO controls (main_control, water_source, circle1, circle2, circle3, circle4) VALUES (". $main_control .", ". $water_source .", ". $circle1 .", ". $circle2 .", ". $circle3 .", ". $circle4 .")";
    
    // instert values into database
    if ($conn->query($sql) === TRUE) {
        echo "New record created succesfully";
    }
    else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
    // exit connetion
    $conn->close();
?>