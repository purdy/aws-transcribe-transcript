# aws-transcribe-transcript
This is a simple utility script to convert the Amazon Transcribe .json transcript into a more readable transcript.

Amazon has a neat Transcription service and you can have the service identify speakers. And in their web interface, they show you a neat play-by-play transcript, but it's limited to the first 5,000 characters. If you want the full transcript, you have to download their JSON file. However, the JSON file only has the transcript as a big block and then some structured data below for the various speakers, start times, and text fragments.

This script creates a transcript that's human-readable.

## Regular Directions

1. Download your Transcription from the Job Details page. The filename format is currently asrOutput.json.
2. Run the `transcript.php` program on the downloaded file, i.e. `php ./transcript.php asrOutput.json`
3. Results will be written in your current working directory as `[FILENAME]-transcript.txt`

## Channel Directions

An optional script has been provided to generate a transcript based on channels. You run the `transcript_ch.php` program and it will generate the results in a `[FILENAME]-transcript_ch.txt` file. Huge thanks to [Joel Varghese](https://github.com/joelprince25) for the contribution!

## Protip

So I use a Mac and I download the asrOutput.json file and it lands in my `~/Downloads` folder. So I use this command from my `aws-transcribe-transcript` folder:

> `mv ~/Downloads/asrOutput.json j.json && php ./transcript.php j.json && cat j.json-transcript.txt | pbcopy`

This will put the transcript in my clipboard so I can paste it into an email response to the person who requested a transcript.
