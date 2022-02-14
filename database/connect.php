<?php

$mysql_host = getenv('mysql_host');
$mysql_user = getenv('mysql_user');
$mysql_pwd = getenv('mysql_pwd');
$mysql_db = getenv('mysql_db');

/*
$server = "3.86.83.200";         # MySQL/MariaDB 伺服器
$dbuser = "cgust";       # 使用者帳號
$dbpassword = "12345678"; # 使用者密碼
$dbname = "cgust-line-project";    # 資料庫名稱
*/

$link = mysqli_connect($mysql_host, $mysql_user, $mysql_pwd);
mysqli_query($link, "SET NAMES 'UTF8'");
mysqli_select_db($link, $mysql_db) or die("fail");

$datas = array();
$sql = "SELECT `個管師_姓名` FROM `個案管理師_基本資料`";

$result = mysqli_query($link,$sql);

// 如果有資料
if ($result) {
    if (mysqli_num_rows($result)>0) {
        while ($row = mysqli_fetch_assoc($result)) {
            $datas[] = $row;
        }
    }
    // 釋放資料庫查到的記憶體
    mysqli_free_result($result);
}
else {
    echo "錯誤訊息: " . mysqli_error($link);
}

if(!empty($result)){
    print($datas);
}
else {
    echo "查無資料";
}
