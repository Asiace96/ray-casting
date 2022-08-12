# Ray Casting Renderer Demo  
A simple interactive program to demonstrate how ray casting works using a DDA (Digital differential analyzer) algorithm on a tile/grid based system.  

![](ray-case-gif-demo.gif)  

Features 3 different settings to decide on a map size, and the ability to move the player and place walls to play around and see the algorithm at work.  
On the left side of the screen you can see the player (yellow dot) and his line of sight with the green lines - these are the casted rays. There are a 120 rays with a FOV of 60 degrees.  
On the right side of the screen you can see the "3D image" drawn from a first person perspective of the player.  

### Notes
- Reused some of the code with modifications from my path-finding-visualizer, so might add the maze generation algorithms here.  
- Source matrial I based myself on - https://lodev.org/cgtutor/raycasting.html - here they disscuss on implementing the algorithm using vector maths which is more elegant but decided on using angle directly because I found it simpler - this guy explains it well - https://www.youtube.com/c/3DSage.  
  
### To Do:
- Add texturing to the blocks/floor/sky and some fun mechanics from path-finding-visualizer in the future.
- Reform the code to a more OOP approach.
