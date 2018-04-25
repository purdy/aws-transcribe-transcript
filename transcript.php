<?php

$file = $argv[1];
$data = json_decode(file_get_contents($file));
$basename = basename($file);

// Load up speaker labels.
$labels = $data->results->speaker_labels->segments;
$speaker_start_times = [];
foreach ($labels as $label) {
  foreach ($label->items as $item) {
    $speaker_start_times[number_format($item->start_time, 3)] = $label->speaker_label;
  }
}

// Now we iterate through items and build the transcript
$items = $data->results->items;
$lines = [];
$line = '';
$speaker = NULL;
foreach ($items as $item) {
  $content = $item->alternatives[0]->content;
  if (property_exists($item, 'start_time')) {
    $current_speaker = $speaker_start_times[number_format($item->start_time, 3)];
  }
  elseif ($item->type == 'punctuation') {
    $line .= $content;
  }
  if ($current_speaker != $speaker) {
    if ($speaker) {
      $lines[] = [
        'speaker' => $speaker,
        'line' => $line,
      ];
    }
    $line = $content;
    $speaker = $current_speaker;
  }
  elseif ($item->type != 'punctuation') {
    $line .= ' ' . $content;
  }
}
// Record the last line since there was no speaker change.
$lines[] = [
  'speaker' => $speaker,
  'line' => $line,
];


// Finally, let's print out our transcript.
$fh = fopen($file . '-transcript.txt', 'w');
foreach ($lines as $line_data) {
  $line = $line_data['speaker'] . ': ' . $line_data['line'];
  fputs($fh, $line . "\n\n");
}
fclose($fh);

/* End of the transcript.php file */
