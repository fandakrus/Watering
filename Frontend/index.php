<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x" crossorigin="anonymous">
    <link href="./style.css" rel="stylesheet">
    <title>Voda</title>
</head>

<body>
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
                    <a class="nav-link" href="./controls.php">Ovládání</a>
                    <a class="nav-link" href="./history.php">Historie</a>
                </div>
            </div>
        </div>
    </nav>
    <div class='d-flex flex-row bd-highlight'>
        <div class="bd-highlight mupperdiv">
            <h2>Poslední zalévání</h2>
            <?php 
            $last_time = $conn->query("SELECT id, end_time FROM watering_history ORDER BY id DESC LIMIT 1");
            while($row = $last_time->fetch_assoc()) {
                $time_last_time = strtotime($row["end_time"]);
                echo '<p class="fs-1 mb-0">' . date("d. m. Y", $time_last_time) . '</p>';
                echo '<p class="fs-1">' . date("H:i", $time_last_time) . '</p>';
            }
            ?>
        </div>
        <div class="bd-highlight mupperdiv">
            <h2>Stav studně</h2>
            <?php 
            $depth = $conn->query("SELECT id, water_height FROM sensors ORDER BY id DESC LIMIT 1");
            while($row = $depth->fetch_assoc()) {
                echo "<p class='mdepth fs-1 mb-0'>". number_format($row["water_height"], 2) ." cm</p>";
            }
            ?>
        </div>
    </div>
    <table class="table table-striped">
        <thead>
            <td>Pořadí</td>
            <td>Hladina</td>
            <td>Vlhost</td>
            <td>Plovák</td>
            <td>Čas</td>
        </thead>
        <tbody>
        <?php
            
            $result = $conn->query("SELECT id, water_height, soil_humidity, float_sensor, meas_date FROM sensors ORDER BY id DESC LIMIT 10");
            $row_counter = 1;
            while($row = $result->fetch_assoc()) {
                if ($row["float_sensor"] == true) {
                    $dot = '<span class="my-active">●</span>';
                } else {
                    $dot = '<span class="my-inactive">●</span>';
                }
                echo "<tr>
                    <td>". $row_counter ."</td>
                    <td>". $row["water_height"] ."</td>
                    <td>". $row["soil_humidity"] ."</td>
                    <td>". $dot ."</td>
                    <td>". $row["meas_date"]. "</td>
                </tr>";
                $row_counter += 1;
            }
            $conn->close;

        ?>
        </tbody>
    </table>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
</body>

</html>