#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import io
# [END import_libraries]
# Revise from Google Speech API Python sample-transcribe.py


class Transcribe:
    def __init__(self, file, language):
        self.language = language
        self.transcripts_list = None
        if file.startswith('gs://'):
            self.transcribe_gcs(file)
        else:
            self.transcribe_file(file)

    def transcribe_file(self, speech_file):
        """Transcribe the given audio file."""
        from google.cloud import speech
        speech_client = speech.Client()

        with io.open(speech_file, 'rb') as audio_file:
            content = audio_file.read()
            audio_sample = speech_client.sample(
                content=content,
                source_uri=None,
                encoding='LINEAR16',
                sample_rate_hertz=16000)

        try:
            alternatives = audio_sample.recognize(self.language)
            self.transcripts_list = [alternative.transcript
                                     for alternative in alternatives]
        except ValueError:
            self.transcripts_list = []

    def transcribe_gcs(self, gcs_uri):
        """Transcribes the audio file specified by the gcs_uri."""
        from google.cloud import speech
        speech_client = speech.Client()

        audio_sample = speech_client.sample(
            content=None,
            source_uri=gcs_uri,
            encoding='FLAC',
            sample_rate_hertz=16000)
        try:
            alternatives = audio_sample.recognize(self.language)
            self.transcripts_list = [alternative.transcript
                                     for alternative in alternatives]
        except ValueError:
            self.transcripts_list = []
