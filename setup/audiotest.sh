echo "Test your audio equipment by speaking into the microphone for 3 seconds"
echo "Press ENTER to beign"
read temp
arecord -d 3 -f cd /tmp/3secondtest.wav
echo "playing back audio test"
aplay -d 3 -f cd /tmp/3secondtest.wav
echo "If you didn't hear anything, you might want to try adjusting your volume levels for your speaker and microphone by running"
echo "alsamixer"

