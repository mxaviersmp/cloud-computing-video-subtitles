from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

class VideoSubtitle( object ):

    def __init__( self ):
        
        self.duration = 0.0
        self.transcription_words = 0
        self.translation_words = 0

        pass

    def __annotate( self, clip, txt_pt, txt_en ):

        font_size = clip.h * 0.05

        num_words_pt = len( txt_pt.split() )
        self.translation_words += num_words_pt

        mult = 2

        if( num_words_pt > 9 ):
            
            aux_pt = txt_pt.split()
            aux_pt.insert( 8, '\n' )

            mult = 4

            txt_pt = " ".join( aux_pt )

        num_words_en = len( txt_en.split() )
        self.transcription_words += num_words_en

        if( num_words_en > 9 ):
            
            aux_en = txt_en.split()
            aux_en.insert( 8, '\n' )

            txt_en = " ".join( aux_en )

        txt_clip_pt = TextClip( txt_pt, font='Amiri-Bold', fontsize=font_size, color='white')
        txt_clip_en = TextClip( txt_en, font='Amiri-Bold', fontsize=font_size, color='white')

        txt_clip_pt = txt_clip_pt.on_color(color=(20,85,33), col_opacity=0.8).set_pos( ("center", clip.h - mult*(font_size + 2)) )
        txt_clip_en = txt_clip_en.on_color(color=(0,0,0), col_opacity=0.8).set_pos( ("center", clip.h - (mult*0.5)*(font_size) ) ) 

        annotated_clip = CompositeVideoClip( [clip, txt_clip_pt, txt_clip_en] )

        return annotated_clip.set_duration(clip.duration)

    def __generateSubs( self, clip, subPath ):

        generator = lambda txt: TextClip(txt, font='Amiri-Bold', fontsize=40, color='white')

        subs = SubtitlesClip( subPath, generator )
        subs = subs.subclip( 0, clip.duration - .001 )
        subs.set_duration( clip.duration - .001 )

        return subs

    def createAnnotatedVideo( self, fileName, originalClipPath, subtitlesPtFilePath, subtitlesEnFilePath, outputFilePath ):

        self.transcription_words = 0
        self.translation_words = 0

        clip = VideoFileClip( originalClipPath )
    
        subs_pt = self.__generateSubs( clip, subtitlesPtFilePath ).in_subclip( t_start = 0 , t_end = 180 )
        subs_en = self.__generateSubs( clip, subtitlesEnFilePath ).in_subclip( t_start = 0 , t_end = 180 )

        annotated_clips = []

        aux = 0

        for ( (from_t, to_t), txt_pt ), ( _, txt_en) in zip(subs_pt, subs_en):

            # if aux == 0:

            #     annotated_clip.append( clip.subclip( aux, from_t) ) 

            if from_t - aux > 0:
                    
                annotated_clips.append( clip.subclip( aux+0.00001, from_t-0.00001) ) 


            annotated_clips.append( self.__annotate(clip.subclip(from_t, to_t), txt_pt, txt_en ) )

            aux = to_t

        #annotated_clips = [ self.__annotate(clip.subclip(from_t, to_t), txt_pt, txt_en ) for ( (from_t, to_t), txt_pt ), ( _, txt_en) in zip(subs_pt, subs_en) ]  

        final_clip = concatenate_videoclips( annotated_clips )
        final_clip.write_videofile(outputFilePath)

        return { 'video_id': fileName,  'duration' : clip.duration, 'transcription_words' : self.transcription_words ,'translation_words' : self.translation_words }