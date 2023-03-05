/*
* Original Code Sourced/inspired From https://www.tutorialspoint.com/how-to-detect-human-faces-in-real-time-in-opencv-using-cplusplus
* Modified and Finalized by Connor Marshall on 3/4/23
*
*/

#include<iostream>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/objdetect/objdetect.hpp>

#include<string>
#include<ctime>
#include<time.h>
#include <stdio.h>     
#include <stdlib.h> 

using namespace std;
using namespace cv;


//directory info
const string IMGDIR = "C:/Users/conno/Documents/hackathon/pythonUploaded/images/";
const string filePrefix = "face";

//delay after sending one snapshot
const int SNAPSHOTDELAY  = 4000;

string statText = "";


int main(int argc, char** argv) {
  

   //matrix to hold frame data
   Mat video_stream;

  //access webcam as VideoCapture object
   VideoCapture real_time(0);

   //creates main window to display tracking
  namedWindow("Face Detector", WINDOW_AUTOSIZE);

  //loading the training source
   string trained_classifier_location = "C:/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml";
   CascadeClassifier faceDetector;
   faceDetector.load(trained_classifier_location);

  //holds detected faces location data
   vector<Rect>faces;
   
  //face cropping matrix and flagged bool
  bool hasCropped = false;
  Mat cropped_face;
  int imgNum = 0;

  clock_t lastTime = clock();


   while (true) {
      clock_t frameTi = clock();

      faceDetector.detectMultiScale(video_stream, faces, 1.1, 4, CASCADE_SCALE_IMAGE, Size(100, 100));
      //real_time.read(video_stream);
      real_time >> video_stream;

      

      //find where in the frame each face is to determing rectangle bounds
      for (int i = 0; i < faces.size(); i++){
         Mat faceROI = video_stream(faces[i]);
         int x = faces[i].x;
         int y = faces[i].y;
         int h = y + faces[i].height;
         int w = x + faces[i].width;
         rectangle(video_stream, Point(x, y), Point(w, h), Scalar(255, 0, 255), 2, 8, 0);


        //crop and save image frame
        if(!hasCropped)
        {
          cropped_face = video_stream(faces[i]);
          imwrite(IMGDIR + filePrefix + std::to_string(imgNum) +".jpg",cropped_face);

          //imshow("Face Detector", cropped_face);
          hasCropped = true;
          imgNum++;

          lastTime = clock();
        }
      }

      //check to disable snapshot cooldown
      if(hasCropped)
      {
        clock_t checkTime = clock();
        if(checkTime - lastTime > SNAPSHOTDELAY)
            hasCropped = false;
      }


      //STAT BAR
      statText = "";

      //add cooldown satus to stat bar
      if(hasCropped)
        statText += "Cooldown: TRUE ";
      else
        statText += "Cooldown: FALSE";

      //adds total pictures saved
      statText += "  Photos Saved: " + to_string(imgNum+1);

      // add latency to stat bar
      clock_t frameTf = clock();
      statText += "    Latency : " + to_string((frameTf -frameTi)) + " ms";
    

      //update info text to the window
      putText(video_stream, statText, Point(20,20),FONT_HERSHEY_COMPLEX, .5,Scalar(0,255,0), 1);

      //update the image to the screen
      imshow("Face Detector", video_stream);
      
      

      int key = waitKey(1);
      //if r is pressed reset image crop
      if(key == 'r')
        hasCropped = false;
      //end if esc is pressed
      else if (key == 27)
        break;

      
   }
   return 0;
}