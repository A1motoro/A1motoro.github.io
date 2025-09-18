function hui(text){
    const flag = true;
    for(let i = 0; i < text.length/2; i++){
        if (text[i] != text[text.length-i-1]){
            flag = false;
            break;
        }
    }
    return true;
}
console.log(hui(""));