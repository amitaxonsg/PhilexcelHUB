<?php
// Fixed executable and entry point: no request value is passed as a command.
declare(strict_types=1);
function unavailable(): never {
    http_response_code(503);
    header('Content-Type: text/plain');
    header('Cache-Control: no-store');
    exit('Philexcel HUB is being prepared. Please try again later.');
}
$hosts = ['ai.philexcel.com','enroll.philexcel.com','admin.philexcel.com','axon.philexcel.com'];
$host = strtolower($_SERVER['HTTP_HOST'] ?? '');
if (!in_array($host, $hosts, true)) { http_response_code(400); exit; }
if (($_SERVER['HTTPS'] ?? '') !== 'on') {
    header('Location: https://' . $host . ($_SERVER['REQUEST_URI'] ?? '/'), true, 302);
    exit;
}
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 16384) { http_response_code(413); exit; }
$body = file_get_contents('php://input', false, null, 0, 16385);
if ($body === false || strlen($body) > 16384) { http_response_code(413); exit; }
$payload = json_encode([
    'host'=>$host, 'uri'=>$_SERVER['REQUEST_URI'] ?? '/',
    'method'=>$_SERVER['REQUEST_METHOD'] ?? 'GET',
    // Ignore forwarded identity headers. Cloudflare client-IP restoration must be
    // performed by the existing trusted Apache configuration, if configured.
    'remote'=>$_SERVER['REMOTE_ADDR'] ?? '', 'body'=>base64_encode($body),
    'content_type'=>$_SERVER['CONTENT_TYPE'] ?? '',
    'cookie'=>$_SERVER['HTTP_COOKIE'] ?? '',
    'csrf'=>$_SERVER['HTTP_X_CSRF_TOKEN'] ?? '', 'accept'=>$_SERVER['HTTP_ACCEPT'] ?? ''
], JSON_THROW_ON_ERROR);
$command = ['/home/philexcel/apps/philexcel-hub/.venv/bin/python', '-I',
    '/home/philexcel/apps/philexcel-hub/portal/cpanel/bridge.py'];
$pipes = [];
$process = proc_open($command, [0=>['pipe','r'],1=>['pipe','w'],2=>['pipe','w']], $pipes,
    '/home/philexcel/apps/philexcel-hub/portal');
if (!is_resource($process)) unavailable();
// Input is bounded below typical pipe capacity; handle partial writes.
$offset = 0;
while ($offset < strlen($payload)) {
    $written = fwrite($pipes[0], substr($payload, $offset));
    if ($written === false || $written === 0) break;
    $offset += $written;
}
fclose($pipes[0]);
stream_set_blocking($pipes[1], false);
stream_set_blocking($pipes[2], false);
$output = ''; $failure = false; $deadline = microtime(true) + 90;
do {
    $output .= stream_get_contents($pipes[1]);
    stream_get_contents($pipes[2]); // Drain without exposing provider errors.
    $state = proc_get_status($process);
    if (strlen($output) > 12*1024*1024 || microtime(true) > $deadline) {
        $failure = true; proc_terminate($process, 9); break;
    }
    if ($state['running']) usleep(10000);
} while ($state['running']);
$output .= stream_get_contents($pipes[1]);
fclose($pipes[1]); fclose($pipes[2]); proc_close($process);
if ($failure || $offset !== strlen($payload)) unavailable();
$response = json_decode($output, true);
if (!is_array($response) || !isset($response['status'], $response['headers'], $response['body'])) unavailable();
$decoded = base64_decode($response['body'], true);
if ($decoded === false || $response['status'] < 200 || $response['status'] > 599) unavailable();
http_response_code($response['status']);
foreach ($response['headers'] as [$name, $value]) {
    if (preg_match('/[\r\n]/', $name.$value)) unavailable();
    if (in_array(strtolower($name), ['connection','transfer-encoding','content-length','server'], true)) continue;
    header($name.': '.$value, false);
}
echo $decoded;
