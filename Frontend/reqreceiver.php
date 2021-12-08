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

    //open object with database
    $conn = OpenDbCon();
    
?>