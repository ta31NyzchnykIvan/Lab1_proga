<?php
// Simple API entrypoint. Serves JSON files from ../data/<topic>.json
// Supports: /data, /data?topic=name, /data/name

// Allow local requests from other tools/clients
header('Access-Control-Allow-Origin: *');

$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Determine topic from path (/data/name) or query (?topic=name). Default: items
$topic = null;
if (preg_match('#^/data(?:/([^/]+))?$#', $uri, $m)) {
	if (!empty($m[1])) {
		$topic = $m[1];
	} elseif (isset($_GET['topic']) && $_GET['topic'] !== '') {
		$topic = $_GET['topic'];
	} else {
		$topic = 'items';
	}
} else {
	http_response_code(404);
	header('Content-Type: application/json');
	echo json_encode(['error' => 'Not found']);
	exit;
}

// sanitize topic (allow letters, numbers, underscore, hyphen)
if (!preg_match('/^[A-Za-z0-9_-]+$/', $topic)) {
	http_response_code(400);
	header('Content-Type: application/json');
	echo json_encode(['error' => 'Invalid topic name']);
	exit;
}

$file = __DIR__ . '/../data/' . $topic . '.json';
if (!file_exists($file)) {
	// list available topics
	$files = glob(__DIR__ . '/../data/*.json');
	$names = array_map(function ($f) {
		return pathinfo($f, PATHINFO_FILENAME);
	}, $files);

	http_response_code(404);
	header('Content-Type: application/json');
	echo json_encode(['error' => 'Topic not found', 'available' => $names]);
	exit;
}

header('Content-Type: application/json');
readfile($file);
exit;
