from glob import glob
from pydub import AudioSegment
import random


def main():
    # Create mime-clip mime-clip

    # path = 'media/'
    # mime_clip = FragmentCollection(path)
    # mime_clip.add_frags_ntimes_each()
    # mime_clip.add_frags_ntimes_each_shuffled()
    # print(mime_clip)
    # mime_clip.export()

    # Hash testing
    
    audio_01 = AudioSegment.from_mp3('tests/hash_01.mp3')
    audio_02 = AudioSegment.from_mp3('tests/hash_02.mp3')
    audio_03 = AudioSegment.from_mp3('tests/hash_03_diff.mp3')
    print(hash(audio_01))
    print(hash(audio_02))
    print(hash(audio_03))


class FragmentCollection:
    def __init__(self, file_or_path, spacer=1.1) -> None:
        self.spacer = spacer
        self.clip = AudioSegment.empty()
        self.frags_filenames = self.load_frags_filenames(file_or_path)
        self.frags = self.load_frags_audio()

    def load_frags_filenames(self, file_or_path):
        '''Uses files or path to return list of files'''
        if isinstance(file_or_path, list):
            return file_or_path
        elif isinstance(file_or_path, str):
            files = [filename for filename in glob(f'{file_or_path}*.mp3')]
            return files

    def load_frags_audio(self):
        '''Uses filenames to load audio to frags list'''
        frags = []
        for mp3_file in self.frags_filenames:
            chunk = AudioSegment.from_mp3(mp3_file)
            if self.spacer:
                spacer = len(chunk)*self.spacer
                chunk += AudioSegment.silent(duration=spacer)
            frags.append(chunk)
        return frags

    def add_frags_ntimes_each(self, times_each=3):
        for frag in self.frags:
            self.clip += frag * times_each

    def add_frags_ntimes_each_shuffled(self, times_each=3):
        local_frags = self.frags * times_each
        random.shuffle(local_frags)
        for frag in local_frags:
            self.clip += frag

    def export(self, output_name='mime-clip'):
        output_name = "output/{}_{}_{}.mp3".format(
            output_name, len(self), random.randrange(1, 100))
        self.clip.export(output_name, format='mp3')

    def __len__(self):
        return int(self.clip.duration_seconds)

    def __repr__(self):
        filenames = '\n'.join(self.frags_filenames)
        return f"lenght: {len(self)} Seconds\nFiles:\n{filenames}"

    def __str__(self):
        filenames_len = len(self.frags_filenames)
        return f"lenght: {len(self)} Seconds\nFiles: {filenames_len}"


if __name__ == '__main__':
    main()
