

# Toucan 
![test](./ui/toucan_icon_100_100.png)

**Toucan** gives your images an artsy low-poly effect.   
We do so by creating a Delauney triangulation over a set of points.  
The points are determined using Poisson disc sampling, SIFT keypoints and a Canny edge detector.

-----
## Gallery

Some examples of results. All original images are from _[unsplash.com](https://unsplash.com/)_


![t1](./doc/gallery/t1_.png)
![t2](./doc/gallery/t2_.png)
![t5](./doc/gallery/t5_.png)
![t6](./doc/gallery/t6_.png)
![t3](./doc/gallery/t3_.png)
![t4](./doc/gallery/t4_.png)

-----
## Walkthrough

The first tab you see when you open the app provides a more thorough explanation for the successive steps.

![toucan_help](./doc/toucan_help.png)

-----
The first step is to load our image in the "Load" tab.  
You will see a uniformly sampled result preview on the right side.
Because of the uniform basis sampling that is being applied, loading the image could take a while. 

![toucan_load](./doc/toucan_load.png)

-----
In the "Uniform" tab we can modify the uniform basis sampling.  
This is done using Poisson disc sampling with a configurable radius:

![toucan_uniform](./doc/toucan_uniform.png)

-----
By sampling the edges using a Canny edge detector, we can bring back a bit more detail:

![toucan_edges](./doc/toucan_edges.png)

-----
Finally to bring back some final highlights we sample some SIFT keypoints:

![toucan_keypoints](./doc/toucan_keypoints.png)

-----
The result is a colored Delauney Triangulation of all points added in the previous steps.  
Don't forget to save your results using the button in the bottom right.  
Have fun!!
