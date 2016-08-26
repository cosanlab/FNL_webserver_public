"""
NOT CURRENTLY FUNCTIONING
I think it's purely an issue with the file manager not finding the video files
Also, FFMPEG will need to be installed on the server

To Add:
call that generates multiple pictures
call that strings the different video clips together
"""

from os import system

from app import app
# except:
#     from __init__ import app, api

def slice(episode, time1, time2):
    #takes in the episode, timepoint, runs ffmpeg from
    #the command line to slice a file named <input> from time1 to time2

    #command used to compress the video file:
    #$ ffmeg -i <inputname.extension> -c:v libx264 -preset medium -s 960x540 <outputname.extension>

    #times should be formatted as '00:00:00.000'

    t1l = [n for n in time1.split(':')]
    t2l = [n for n in time2.split(':')]
    t1 = ''
    t2 = ''
    for n in range(0, 3):
        if n < 2:
            t1 += t1l[n]
            t1 += ','
        else:
            t1 += t1l[n]
    for n in range(0, 3):
        if n < 2:
            t2 += t2l[n]
            t2 += ','
        else:
            t2 += t2l[n]


    if episode == 'ep1':
        """Throws error from moment in Jinja; interprets title as a timestamp"""
        system('ffmpeg -i episodes/FNL_01_960x540_h264_med.mp4 -y -ss %s -to %s %s.mp4'%(time1, time2, ('server/templates/ep1'+'-'+t1+'_to_'+t2)))
        return ('ep1'+'-'+t1+'_to_'+t2+'.mp4')
        """Used for tesing the video loading; outputs using the same filename for all clips"""
        # system('ffmpeg -i episodes/FNL_01_960x540_h264_med.mp4 -y -ss %s -to %s %s'%(time1, time2, ('server/templates/ep1_mostrecent.mp4')))
        # return ('ep1_mostrecent.mp4')
    else:
        return "Couldn't interpret '%s'; use 'ep#'(ep1, ep2, etc.)"%episode

def framegrab(episode, time):

    #automatically removes framegrabs folder and contents, then creates a new folder
    # system('cd server')
    # system('rmdir -f framegrabs')
    # system('cd ..')
    # system('mkdir server/framegrabs')

    system('ls')

    t1l = [n for n in time.split(':')]
    t1 = ''
    for n in range(0, 3):
        if n < 2:
            t1 += t1l[n]
            t1 += '_'
        else:
            t1 += t1l[n]

    if episode == 'ep1':
        #somewhat finicky; no '/' when giving the file path
        system('ffmpeg -ss %s -i FNL_Videos/FNL_01.mp4 -an framegrabs/%s.jpg'%(time, ('ep1-'+t1)))
        system('ls')
        return 'framegrabs/%s.jpg'%('ep1-'+t1)
    else:
        return "Couldn't interpret '%s'; use 'ep#'(ep1, ep2, etc.)"%episode

    #working dummy script (saves to the desktop; expects file on the desktop)
    #system('ffmpeg -i Desktop/FNL_01_960x540_h264_med.mp4 -ss 00:00:12.0 -to 00:00:14.0 Desktop/testout.mp4')