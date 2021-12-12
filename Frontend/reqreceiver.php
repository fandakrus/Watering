<?php
    function OpenDbCon() {
        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "watering";
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
    }

    if($circle1 == "true" or $circle2 == "true" or $circle3 == "true" or $circle4 == "true") {
        $main_control = "true";
    } else {
        $main_control = "false";
    }

    $sql = "INSERT INTO controls (main_control, circle1, circle2, circle3, circle4) VALUES (". $main_control .", ". $circle1 .", ". $circle2 .", ". $circle3 .", ". $circle4 .")";
    
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