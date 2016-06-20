import hiero
import csv
import os

class LineupSheet(object):

    def __init__(self):
        self.target_video_track = 'Video 1'
        self.viewer = hiero.ui.currentViewer()
        self.cur_sequence = self.viewer.player().sequence()
        self.start_frame = self.cur_sequence.timecodeStart()
        self.track = self.get_track_by_name(self.target_video_track)
        self.project = self.track.project()

    def get_track_by_name(self, name):
        for i in self.cur_sequence.items():
            if i.name() != name:
                continue
            return i
        return None

    def export_to_csv(self):

        output_file = os.path.join(self.project.projectRoot(), self.track.name() + '.csv')

        csvfile = open(output_file, 'wt')
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(('Shot Name', 'Source Filename', 'Timecode In', 'Timecode Out', 'Frame Range'))

        for i in self.track.items():
            shot_name = i.name()
            frame_in = i.timelineIn()
            frame_out = i.timelineOut()
            clip = i.source()
            source = clip.mediaSource()
            source_name = source.filename()
            tc = hiero.core.Timecode()
            tb = hiero.core.TimeBase.k24
            time_in = '%02d:%02d:%02d:%02d' % tc.framesToHMSF(frame_in + self.start_frame, tb, False)
            time_out = '%02d:%02d:%02d:%02d' % tc.framesToHMSF(frame_out + self.start_frame, tb, False)
            duration = i.duration()

            print 'Shot name: ', shot_name
            print 'Timeline In: ', time_in
            print 'Timeline Out: ', time_out
            print 'Duration: ', duration
            print 'Source file name: ', source_name

            csvwriter.writerow((shot_name, source_name, time_in, time_out, duration))

        csvfile.close()
