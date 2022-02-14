<?php

$mysql_host = getenv('mysql_host');
$mysql_user = getenv('mysql_user');
$mysql_pwd = getenv('mysql_pwd');
$mysql_db = getenv('mysql_db');

$link = mysqli_connect($mysql_host, $mysql_user, $mysql_pwd);
if (!$link) {
    die("資料庫連接失敗: " . mysqli_connect_error());
}

mysqli_query($link, "SET NAMES 'UTF8'");
mysqli_select_db($link, $mysql_db) or die("fail");
