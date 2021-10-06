let labels = document.getElementsByTagName('label')

$('<span></span>').insertAfter('input')
for(let i=0; i<labels.length; i++){
    labels[i].className = 'radio radio-primary'
    labels[i].style.height = '50px'
    labels[i].style.fontSize = '15px'
    console.log(labels[i])
}