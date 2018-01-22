
pics_loc = ' /pics';
file_names =[];  // holds all the file names


for (i=0;i<file_names.length;i++){
newdiv = document.createElement("div");  // create a div
newdiv.className = "img_div";
newdiv.style.width = "200px";
newdiv.style.height = "200px";
newdiv.style.display = "inline-block";
newdiv.style.padding = "2px";


newimg = document.createElement("img");    // create img tag
newimg.src ='https://via.placeholder.com/500x500';
newimg.className='imgs';
newimg.style.width = "200px";
newimg.style.height = "200px";

newdiv.appendChild(newimg);

img_container = document.querySelector("#my_imgs");
img_container.appendChild(newdiv);

}


// code for click next and prev button
var b = document.querySelector(".mybutton");
b[0].addEventListener('click', dec);
b[1].addEventListener('click', inc);

function inc(){
  n=1;   // right button
 curr_img += n;
 display_imgs(curr_img);
}

function dec(){
    n=-1;  //left button
 curr_img += n;
 display_img(curr_img);
}



//display the image in full

function display_img(k){
var x  = document.querySelector(".img_div");

  if (n > x.length) {k = 1;}
  if (n < 1) {l = k.length;}
 for (i = 0; i < imgs.length; i++) {
     x[i].style.display = "none";
  }
  x[k-1].style.display = "block";
}