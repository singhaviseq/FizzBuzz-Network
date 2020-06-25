# FizzBuzz-Network using PyTorch
Have you ever played the game FizzBuzz.? 
This game has been used as a fun example by ![Joel Grus](http://joelgrus.com/2016/05/23/fizz-buzz-in-tensorflow/) ( Research Engineer at AI2 ) , which teaches children about Division. 

### Problem Framing:

We formulate the problem as simple classification task where the problem classifies the output to different categories :
* fizz  - *If the number is divisible by 5*
* 'buzz' - *If the number is divisible by 3*
* 'FizzBuzz' - *If the number is divisible by both 5 & 3
* 'No Change' - *If the number is divisible by none of 5 or 3

We also converted the input number to binary-encoded form, which is easier for the network to process than whole numbers.

Although this particular example doesn't solve any practical problem but it's a fun way to see how a Neural Net works. As I've been learning PyTorch, I decided to give it's implementation a try.
