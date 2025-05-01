document.getElementById("aiForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Sayfanın yeniden yüklenmesini engelle

    // Form verilerini al
    let input = document.getElementById("floatingTextarea2").value;

    // Doğru email ve şifre

    if (input == "") {
        // Başarılı giriş
        let yanlis = document.getElementById("message");
        yanlis.innerHTML = `Lütfen Bir Boş Geçmeyin`;
    } else {
        // Hatalı giriş
        let yanlis = document.getElementById("message");
        yanlis.innerHTML = "Harika";
    }
});
