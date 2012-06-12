var photos = [
   {filename:'1.jpg',width:640,height:360,caption:"Grammar is important, kids!",thumbnail:'http://i.imgur.com/HuJQul.jpg'},
    {filename:'2.jpg',width:640,height:360,caption:"Yes, I'm looking for a stock photogr",thumbnail:'http://i.imgur.com/L5PVml.jpg'},
    {filename:'3.png',width:640,height:360,caption:"This just happened like an hour ago.",thumbnail:'http://i.imgur.com/QOySql.jpg'},
    {filename:'4.jpg',width:640,height:360,caption:"",thumbnail:'http://i.imgur.com/mq8ocl.jpg'},
    {filename:'5.jpg',width:640,height:360,caption:"Damn you autocorrect...",thumbnail:'http://i.imgur.com/rTKGSl.jpg'},
    {filename:'6.jpg',width:640,height:360,caption:"Damn you autocorrect...",thumbnail:'http://i.imgur.com/Ht3Zvl.jpg'},
    {filename:'7.jpg',width:640,height:360,caption:"Damn you autocorrect...",thumbnail:'http://i.imgur.com/Txhuvl.jpg'},
    {filename:'8.jpg',width:640,height:492,caption:"Damn you autocorrect...",thumbnail:'http://i.imgur.com/h3Vgll.jpg'},
    {filename:'9.jpg',width:640,height:360,caption:"Kill Me.",thumbnail:'http://i.imgur.com/90LoQl.jpg'},
    {filename:'10.png',width:640,height:360,caption:"College Lectures",thumbnail:'http://i.imgur.com/3httVl.jpg'},
    {filename:'11.png',width:546,height:510,caption:"One Megabite",thumbnail:'http://i.imgur.com/LSROHl.jpg'},
    {filename:'12.png',width:640,height:360,caption:"Why Youtube never fails to amaze me.",thumbnail:'http://i.imgur.com/h09BMl.jpg'},
    {filename:'13.jpg',width:640,height:400,caption:"Confused Kitty",thumbnail:'http://i.imgur.com/Xy2xil.jpg'},
    {filename:'14.jpg',width:640,height:360,caption:"The power.",thumbnail:'http://i.imgur.com/KzK1El.jpg'},
    {filename:'15.jpg',width:640,height:360,caption:"Om nom nom.",thumbnail:'http://i.imgur.com/TtPFal.jpg'},
    {filename:'16.jpg',width:640,height:360,caption:"Never gets old",thumbnail:'http://i.imgur.com/pH2R9l.jpg'},
    {filename:'17.jpg',width:640,height:360,caption:"Fry on Chuck Testa",thumbnail:'http://i.imgur.com/Acnnil.jpg'}
];

var jg = new JGlance({
        container: $('#results'),
        maxPerRow: 4,
        photoErrorCallback: function (photo, img) {
            img.attr( 'src', 'http://placehold.it/350x150' ).addClass( 'broken-image' );
        }
    });
// we pass the photos via 'push' method
jg.push( photos );

