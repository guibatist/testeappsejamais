window.addEventListener("scroll", function(){
    let header = this.document.querySelector('#header');
    let logo = this.document.querySelector('.logo'); // Selecionando o elemento com a classe "logo"
    
    header.classList.toggle('rolagem', window.scrollY > 0);
    
    // Modificando o estilo do elemento com a classe "logo" com base na posição de rolagem
    if (window.scrollY > 0) {
        logo.style.color = '#000000'; // ou qualquer outra cor desejada
    } else {
        logo.style.color = '#000000'; // ou qualquer outra cor desejada para quando o cabeçalho não estiver rolado
    }
});
