<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
    <link href="./main.css" rel="stylesheet">
    <title>Voda</title>
</head>

<body>
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

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-link active" aria-current="page" href="./index.php">Domov</a>
                    <a class="nav-link" href="./control.php">Ovládání</a>
                    <a class="nav-link" href="#">Historie</a>
                </div>
            </div>
        </div>
    </nav>
    <div class='d-flex flex-row bd-highlight'>
        <div class="bd-highlight mupperdiv">
            <h2>Poslední zalévání</h2>
            <p class="fs-1 mb-0">12. 6. 2021</p>
            <p class="fs-1">5:00</p>
        </div>
        <div class="bd-highlight mupperdiv">
            <h2>Stav studně</h2>
            <?php 
            $depth = $conn->query("SELECT id, water_height FROM sensors ORDER BY id DESC LIMIT 1");
            while($row = $depth->fetch_assoc()) {
                echo "<p class='mdepth'>". $row["water_height"] ." m</p>";
            }
            ?>
        </div>
    </div>
    <table class="table table-striped">
        <th>
            <td>Pořadí</td>
            <td>Hladina</td>
            <td>Vlhost</td>
            <td>Plovák</td>
            <td>Čas</td>
        </th>
        
        <?php
            
            $result = $conn->query("SELECT id, water_height, soil_humidity, float_sensor FROM sensors ORDER BY id DESC LIMIT 10");
            $row_counter = 1;
            while($row = $result->fetch_assoc()) {
                echo "<tr>
                    <td>". $row_counter ."</td>
                    <td>". $row["water_height"] ."</td>
                    <td>". $row["soil_humidity"] ."</td>
                    <td>". $row["float_sensor"] ."</td>
                    <td> 5 </td>
                </tr>";
                $row_counter += 1;
            }
            $conn->close;

        ?>
        
    </table>
</body>

</html>