'''
Created on Feb 2, 2018

@authors: Danny Le, Jeffrey Pham, Kevon Nguyen 
'''

import soundcloud
import soundhub
import webbrowser

class Engine:
    
    def __init__(self):
        self.client = soundcloud.Client(client_id="MgT8dvRJVcFR9fI5Szar82usLfSQdg3n")
        self.data = []
    
    def read_file_create_list(self):
        track_list = []
        with open('track_ids.txt', 'r') as myFile:
            data = myFile.readlines() 
            for i in data:
                track_list.append(i)
        return track_list


    def id_list_to_html_list(self,track_id):
        html_list = []
        for i in track_id:
            track = self.client.get('/tracks/'+str(i).strip())
            track_url = track.permalink_url
        
            embeded_info = self.client.get('/oembed', url = track_url)
            html_list.append(embeded_info.obj['html'])
            
        return html_list
            
    def create_file_from_html_list(self,widget_list,track_list,filename,imagename):
        file = open(filename, "w", encoding='utf-8')

        # image header here
        file.write('<link rel="stylesheet" type="text/css" href="style.css"><style type="text/css"></style>\n')
        file.write('<header><img src = "'+imagename+'"></header>\n')
        file.write('<body>\n')
        for i in range(0,len(widget_list)):
            file.write(str(widget_list[i]))
            file.write('\n')

            # liked by here 
            users = str(" » ".join(track_list[i][2]))
            liked_by = "╚» LIKED BY: " + users; 
            
            file.write(liked_by)
            file.write('\n')
        file.write('</body>')

    def open_html_file(self, filename):
        webbrowser.open_new_tab(filename);
  
    
if __name__ == '__main__':

    ID = soundhub.id_from_input()
    track_dict = soundhub.generate_track_dict(ID)
    track_list = soundhub.generate_sorted_match_list(track_dict)
    soundhub.print_list(track_list)

    new_list = []
    for item in track_list:
        new_list.append(item[0])

    sh = Engine()
    html_list = sh.id_list_to_html_list(new_list)

    filename = "result.html"
    imagename = "logo.png"
    sh.create_file_from_html_list(html_list,track_list,filename,imagename)
    sh.open_html_file(filename)
