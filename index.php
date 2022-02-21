<?php

/**
 * Copyright 2020 GoneTone
 *
 * Line Bot
 * 範例 Example Bot 執行主文件
 *
 * 此範例 GitHub 專案：https://github.com/GoneToneStudio/line-example-bot-tiny-php
 * 此範例教學文章：https://blog.reh.tw/archives/988
 *
 * 官方文檔：https://developers.line.biz/en/reference/messaging-api/
 */

date_default_timezone_set("Asia/Taipei"); //設定時區為台北時區

$channelAccessToken = getenv('line_channel_access_token');
$channelSecret = getenv('line_channel_secret');

$message = null;
$event = null;

$client = new LINEBotTiny($channelAccessToken, $channelSecret);

foreach ($client->parseEvents() as $event) {
    switch ($event['type']) {
        case 'message': //訊息觸發
            $Payload = [ 
                'replyToken' => $event['replyToken'],
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
        case 'postback': //postback 觸發
            //require_once('postback.php'); //postback
            break;
        case 'follow': //加為好友觸發
            $client->replyMessage(array(
                'replyToken' => $event['replyToken'],
                'messages' => array(
                    array(
                        'type' => 'text',
                        'text' => '您好，這是一個範例 Bot OuO
                                    範例程式開源至 GitHub (包含教學)：
                                    https://github.com/GoneTone/line-example-bot-php'
                    )
                )
            ));
            break;
        case 'join': //加入群組觸發
            $client->replyMessage(array(
                'replyToken' => $event['replyToken'],
                'messages' => array(
                    array(
                        'type' => 'text',
                        'text' => '大家好，這是一個範例 Bot OuO
                                    範例程式開源至 GitHub (包含教學)：
                                    https://github.com/GoneTone/line-example-bot-php'
                    )
                )
            ));
            break;
        default:
            //error_log("Unsupporeted event type: " . $event['type']);
            break;
    }
}
