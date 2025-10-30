<?php
// index.php - YT-DLP Audio URL API
header('Content-Type: text/plain; charset=utf-8');
header('Access-Control-Allow-Origin: *');

$videoId = $_GET['v'] ?? '';
if (!preg_match('/^[a-zA-Z0-9_-]{11}$/', $videoId)) {
    http_response_code(400);
    exit('Invalid YouTube ID');
}

$cmd = "yt-dlp -f 'bestaudio/best' --get-url " . escapeshellarg("https://www.youtube.com/watch?v=" . $videoId);
$url = trim(shell_exec($cmd));

if (!$url || strpos($url, 'http') !== 0) {
    http_response_code(500);
    exit('Failed to get URL');
}

echo $url;
