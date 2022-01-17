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
    
    <table class="table table-striped">
        <thead>
            <td>Okruh</td>
            <td>Začátek</td>
            <td>Konec</td>
        </thead>
        <tbody>
        <?php
            
            $result = $conn->query("SELECT id, start_time, end_time, circle FROM watering_history ORDER BY id DESC LIMIT 20");
            $row_counter = 1;
            while($row = $result->fetch_assoc()) {
                echo "<tr>
                    <td>". $row_counter ."</td>
                    <td>". $row["circle"] ."</td>
                    <td>". $row["start_time"] ."</td>
                    <td>". $row["end_time"] ."</td>
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