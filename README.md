<h1 align="center"> KRYPTOZ </h1>
<p align="center" > <img src="https://github.com/vishal-1408/KRYPTOZ/blob/master/img/krytpoz7.PNG" width="200" height="200"> </p>
<hr>

# What is it?
Chat rooms application with end-to-end encryption. This project uses the methodology suggested in WhatsApp technical paper for implementing the end-to-end encryption functionality.

# Sneak Peak

<img src="https://github.com/vishal-1408/KRYPTOZ/blob/master/img/krytpoz1.PNG" width="400" height="400">  <img src="https://github.com/vishal-1408/KRYPTOZ/blob/master/img/krytpoz2.PNG" width="400" height="400"> 
 <img src="https://github.com/vishal-1408/KRYPTOZ/blob/master/img/krytpoz3.PNG" width="400" height="400">  <img src="https://github.com/vishal-1408/KRYPTOZ/blob/master/img/krytpoz5.PNG" width="400" height="400">  <img src="https://github.com/vishal-1408/KRYPTOZ/blob/master/img/krytpoz6.PNG" width="800" height="400"> 
 
 # Cryptography Algorithms Used
 
<ul> 
    <li> 
       <h4>Hashing</h4> 
       <div> 
         Hashing function used in Kryptoz is SHA-256 and it is used to hash the passwords of the users.
       </div>
    </li>
    <li> 
       <h4>AES (GCM)</h4> 
        <div> 
          AES in Galois Control Mode (GCM) is used for the generation of the
          Secret Sender Key. This is the key used for encrypting the messages
        </div>
    </li>
    <li> 
    <h4>ECDH</h4> 
    <div> 
      Elliptic Curve Diffie Hellman (ECDH) key exchange is implemented
      using pycryptodome and the keys for the users will be created 
      when the user signs up and these are the keys used for key exchange process.
    </div>
  </li>
</ul>
 
 <hr>
 <h4 align="center"> Made with :heart:</h4> 






