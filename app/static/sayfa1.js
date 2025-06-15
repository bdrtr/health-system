document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const role = document.getElementById("role").value;
    const errorDiv = document.getElementById("errorMsg");
  
    if (!email || !password || !role) {
      errorDiv.textContent = "Lütfen tüm alanları eksiksiz doldurun.";
      return;
    }
  
    if (email !== "test@example.com" || password !== "123456") {
      errorDiv.textContent = "E-posta ya da şifre hatalı.";
      return;
    }
  
    errorDiv.textContent = "";
    alert(`${role} olarak başarıyla giriş yapıldı.`);
  });
  
  document.getElementById("forgot").addEventListener("click", function (e) {
    e.preventDefault();
    alert("Şifre sıfırlama özelliği henüz aktif değil.");
  });
  
  // "Kayıt Ol" linkine tıklama olayını dinle
document.getElementById('register').addEventListener('click', function(event) {
  event.preventDefault(); // Linkin varsayılan davranışını engelle
  window.location.href = 'sayfa2.html'; // Kayıt sayfasına yönlendir
});
z
  