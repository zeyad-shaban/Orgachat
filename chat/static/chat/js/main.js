document.addEventListener('DOMContentLoaded', function () {
    // -------Add to homepage--------
    try{let deferredPrompt;const addBtn=document.querySelector('#addToHomescreen');addBtn.style.display='none';window.addEventListener('beforeinstallprompt',(e)=>{e.preventDefault();deferredPrompt=e;addBtn.style.display='block';addBtn.addEventListener('click',(e)=>{addBtn.style.display='none';deferredPrompt.prompt();deferredPrompt.userChoice.then((choiceResult)=>{if(choiceResult.outcome==='accepted'){console.log('User accepted the A2HS prompt');var xhr=new XMLHttpRequest()
xhr.open("GET","/metrics/user_installed/",true)
xhr.send()}else{console.log('User dismissed the A2HS prompt');}
deferredPrompt=null;});});});}catch(error){}

    // ------------------
    // HEADER
    // ------------------

    // ---------Navbar----------
    document.querySelector('body').style.paddingTop = document.querySelector('.navbar').clientHeight + 'px'
    // detect scroll top or down
    try{var last_scroll_top=0;window.onscroll=function(){scroll_top=this.scrollY;if(scroll_top<last_scroll_top){document.querySelector('.navbar-main').classList.remove('scrolled-down');document.querySelector('.navbar-main').classList.add('scrolled-up');}else{document.querySelector('.navbar-main').classList.remove('scrolled-up');document.querySelector('.navbar-main').classList.add('scrolled-down');}
last_scroll_top=scroll_top;};}catch(error){}

})

var x=document.getElementById("toast")
var d=document.getElementById("toastDesc")
var tn=document.getElementById("toastNotif")
function toast(txt){tn.play()
d.textContent=txt
x.className="show";setTimeout(function(){x.className=x.className.replace("show","");},5000);}
var backdrop=document.getElementById('backdrop')
function openModal(dataTarget){let modal=document.querySelector(dataTarget)
backdrop.style.display='block'
modal.style.display='block'
modal.classList.add('show')}
function closeModal(dataTarget){let modal=document.querySelector(dataTarget);backdrop.style.display='none';modal.style.display='none';modal.classList.remove('show');}
function toggleDropdown(dataTarget){let dropdown=document.querySelector(dataTarget)
if(dropdown.style.display=='block'){dropdown.style.display='none'}else{dropdown.style.display='block'}};function toggleCollapse(dataTarget){let collapseItem=document.querySelector(dataTarget)
if(collapseItem.classList.contains('show')){collapseItem.classList.remove('show')}else{collapseItem.classList.add('show')}}
function toggleAllCollapse(dataTarget){let collapseItem=document.querySelector(dataTarget)
if(collapseItem.classList.contains('show')){collapseItem.classList.remove('show')}else{collapseItem.classList.add('show')}
let allCollapseItems=document.querySelectorAll(".collapse:not("+dataTarget+")")
for(collapse of allCollapseItems){collapse.classList.remove("show")}}