<?php

$file = $argv[1];
$data = json_decode(file_get_contents($file));
$basename = basename($file);

// Load up channel labels.
$labels = $data->results->channel_labels->channels;
$channel_start_times = [];
foreach ($labels as $label) {
  foreach ($label->items as $item) {
    $channel_start_times[number_format($item->start_time, 3)] = $label->channel_label;
  }
}

// Now we iterate through items and build the transcript
$items = $data->results->items;
$lines = [];
$line = '';
$time = 0;
$channel = NULL;
foreach ($items as $item) {
  $content = $item->alternatives[0]->content;
  if (property_exists($item, 'start_time')) {
    $current_channel = $channel_start_times[number_format($item->start_time, 3)];
  }
  elseif ($item->type == 'punctuation') {
    $line .= $content;
  }
  if ($current_channel != $channel) {
    if ($channel) {
      $lines[] = [
        'channel' => $channel,
        'line' => $line,
        'time' => $time,
      ];
    }
    $line = $content;
    $channel = $current_channel;
    $time = number_format($item->start_time, 3, '.', '');
  }
  elseif ($item->type != 'punctuation') {
    $line .= ' ' . $content;
  }
}
// Record the last line since there was no channel change.
$lines[] = [
  'channel' => $channel,
  'line' => $line,
  'time' => $time,
];


// Finally, let's print out our transcript.
$fh = fopen($file . '-transcript_ch.txt', 'w');
foreach ($lines as $line_data) {
  $line = '[' . gmdate('H:i:s', $line_data['time']) . '] ' . $line_data['channel'] . ': ' . $line_data['line'];
  fputs($fh, $line . "\n\n");
}
fclose($fh);

/* End of the transcript_ch.php file */
