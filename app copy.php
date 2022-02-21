<?php 
 
//設定Token 
$ChannelAccessToken = getenv('line_channel_access_token');
$ChannelSecret = getenv('line_channel_secret');

//讀取資訊 
$HttpRequestBody = file_get_contents('php://input'); 
$HeaderSignature = $_SERVER['HTTP_X_LINE_SIGNATURE']; 
 
//驗證來源是否是LINE官方伺服器 
$Hash = hash_hmac('sha256', $HttpRequestBody, $ChannelSecret, true); 
$HashSignature = base64_encode($Hash); 
if($HashSignature != $HeaderSignature) 
{ 
    die('hash error!'); 
} 
 
//解析 
$DataBody=json_decode($HttpRequestBody, true); 
 
//逐一執行事件 
foreach($DataBody['events'] as $Event) 
{ 
    //當bot收到任何訊息 
    if($Event['type'] == 'message') 
    { 
        $Payload = [ 
            'replyToken' => $Event['replyToken'],
            'messages' => [
                [
                    'type' => 'text',
                    'text' => '我收到你的訊息了'
                ]
            ]
        ];
 
        // 傳送訊息
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://api.line.me/v2/bot/message/reply');
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($Payload));
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $ChannelAccessToken
        ]);
        $Result = curl_exec($ch);
        curl_close($ch);
    }
}
 
?>