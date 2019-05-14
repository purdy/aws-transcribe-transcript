#!/usr/bin/env python3
def main():
	import sys
	import json
	import datetime
	
	filename=sys.argv[1]
	print ("Filename: ", filename)
	with open(filename+'.txt','w') as w:
		with open(filename) as f:
			data=json.loads(f.read())
			labels = data['results']['speaker_labels']['segments']
			speaker_start_times={}
			for label in labels:
				for item in label['items']:
					speaker_start_times[item['start_time']] =item['speaker_label']
			items = data['results']['items']
			lines=[]
			line=''
			time=0
			speaker='null'
			i=0
			for item in items:
				i=i+1
				content = item['alternatives'][0]['content']
				if item.get('start_time'):
					current_speaker=speaker_start_times[item['start_time']]
				elif item['type'] == 'punctuation':
					line = line+content
				if current_speaker != speaker:
					if speaker:
						lines.append({'speaker':speaker, 'line':line, 'time':time})
					line=content
					speaker=current_speaker
					time=item['start_time']
				elif item['type'] != 'punctuation':
					line = line + ' ' + content
			lines.append({'speaker':speaker, 'line':line,'time':time})
			sorted_lines = sorted(lines,key=lambda k: float(k['time']))
			for line_data in sorted_lines:
				line='[' + str(datetime.timedelta(seconds=int(round(float(line_data['time']))))) + '] ' + line_data.get('speaker') + ': ' + line_data.get('line')
				w.write(line + '\n\n')


if __name__ == '__main__':
	main()
