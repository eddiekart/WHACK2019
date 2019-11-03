using Google.Cloud.TextToSpeech.V1;
using System;
using System.IO;

namespace TextToSpeechApiDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            var client = TextToSpeechClient.Create();

            // The input to be synthesized, can be provided as text or SSML.
            var input = new SynthesisInput
            {
                Text = "Whoa whoa there, " + args[0] + "! Killer here is having a fit, so come back later"
            };

            // Build the voice request.
            var voiceSelection = new VoiceSelectionParams
            {
                LanguageCode = "en-US",
                SsmlGender = SsmlVoiceGender.Neutral
            };

            // Specify the type of audio file.
            var audioConfig = new AudioConfig
            {
                AudioEncoding = AudioEncoding.Mp3
            };

            // Perform the text-to-speech request.
            var response = client.SynthesizeSpeech(input, voiceSelection, audioConfig);
            
            // Write the response to the output file.
            using (var output = File.Create("output3.mp3"))
            {
                response.AudioContent.WriteTo(output);
            }
            Console.WriteLine("Audio content written to file \"output3.mp3\"");
        }
    }
}